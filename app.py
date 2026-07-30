"""Water bill distribution application using Kivy."""

import os
import threading
import webbrowser

from kivy.app import App  # type: ignore
from kivy.clock import Clock  # type: ignore
from kivy.lang import Builder  # type: ignore
from kivy.uix.boxlayout import BoxLayout  # type: ignore
from kivy.uix.label import Label  # type: ignore

from database import buscar_unidades
from pdf_generator import gerar_relatorio_pdf

# Descarrega o KV antigo e carrega a versão atualizada explicitamente
# Builder.unload_file("rateio.kv")  # type: ignore
# Builder.load_file("rateio.kv")  # type: ignore

KV_DESIGN = """
<RootLayout>:
    orientation: 'vertical'
    padding: 20
    spacing: 15

    # --- Header ---
    BoxLayout:
        size_hint_y: None
        height: '40dp'
        Label:
            text: 'Gestão de Água - Rateio'
            font_size: '22sp'
            bold: True
            halign: 'left'
            valign: 'middle'
            text_size: self.size

    # --- Input Form ---
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: '40dp'
        spacing: 10

        TextInput:
            id: txt_mes
            hint_text: 'Mês/Ano (ex: 07/2026)'
            multiline: False
            write_tab: False
            on_text_validate: txt_fixo.focus = True

        TextInput:
            id: txt_fixo
            hint_text: 'Custo Fixo Total (R$)'
            multiline: False
            input_filter: 'float'
            write_tab: False
            on_text_validate: txt_var.focus = True

        TextInput:
            id: txt_var
            hint_text: 'Custo Variável Total (R$)'
            multiline: False
            input_filter: 'float'
            write_tab: False
            on_text_validate: root.calcular_rateio()

    # --- Action Buttons ---
    BoxLayout:
        size_hint_y: None
        height: '45dp'
        spacing: 10

        Button:
            id: btn_processar
            text: 'Processar Rateio'
            on_release: root.calcular_rateio()

        Button:
            id: btn_download
            text: 'Baixar PDF'
            disabled: True
            on_release: root.baixar_pdf()

    # --- Output Area (Scrollable) ---
    ScrollView:
        do_scroll_x: False
        BoxLayout:
            id: container_resultados
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            spacing: 8
            padding: [0, 10, 0, 10]
"""

Builder.load_file('layout_agua.kv')


class RootLayout(BoxLayout):
    """Root layout for the water bill distribution application."""

    pdf_path: str = ""

    def calcular_rateio(self) -> None:
        """Inicia o cálculo do rateio em uma thread separada para não travar a UI."""
        self.ids.btn_processar.disabled = True
        self.ids.btn_download.disabled = True

        container = self.ids.container_resultados
        container.clear_widgets()
        container.add_widget(
            Label(
                text="Carregando dados do Supabase...",
                size_hint_y=None,
                height=30,
                color=(0.8, 0.8, 0.8, 1),
            )
        )

        threading.Thread(target=self._processar_async, daemon=True).start()

    def _processar_async(self) -> None:
        """Executa a busca dos dados e cálculos fora da thread principal."""
        mes_ref = self.ids.txt_mes.text.strip() or "07/2026"
        val_fixo_str = self.ids.txt_fixo.text.replace(",", ".").strip()
        val_var_str = self.ids.txt_var.text.replace(",", ".").strip()

        val_fixo = float(val_fixo_str) if val_fixo_str else 0.0
        val_var = float(val_var_str) if val_var_str else 0.0

        try:
            unidades = buscar_unidades()

            Clock.schedule_once(
                lambda dt: self._renderizar_resultados(
                    unidades, val_fixo, val_var, mes_ref
                )
            )
        except (ValueError, ConnectionError, OSError, RuntimeError) as ex:
            Clock.schedule_once(
                lambda dt: self._mostrar_erro(f"Erro ao conectar/buscar dados: {ex}")
            )

    def _renderizar_resultados(
        self, unidades: list, val_fixo: float, val_var: float, mes_ref: str
    ) -> None:
        """Renderiza as informações na UI (Thread Principal)."""
        container = self.ids.container_resultados
        container.clear_widgets()
        self.ids.btn_processar.disabled = False

        if not unidades:
            container.add_widget(
                Label(
                    text="Nenhuma unidade encontrada no Supabase.",
                    color=(1, 0, 0, 1),
                    size_hint_y=None,
                    height=30,
                )
            )
            return

        try:
            total_moro = sum(int(u.get("moradores", 0)) for u in unidades)
            t_fixa = val_fixo / len(unidades) if unidades else 0.0
            t_var = val_var / total_moro if total_moro > 0 else 0.0

            header_lbl = Label(
                text=f"[b]RATEIO - {mes_ref}[/b]",
                markup=True,
                size_hint_y=None,
                height=30,
                halign="left",
                valign="middle",
                text_size=(self.width - 20, None),
            )
            container.add_widget(header_lbl)

            for u in sorted(unidades, key=lambda x: str(x.get("id", "0"))):
                moro = int(u.get("moradores", 0))
                valor_total = t_fixa + (t_var * moro)

                texto_item = (
                    f"Unid {u.get('id')} - {u.get('nome_responsavel')} | "
                    f"{moro} morador(es) | Total: R$ {valor_total:.2f}"
                )

                item_lbl = Label(
                    text=texto_item,
                    size_hint_y=None,
                    height=25,
                    halign="left",
                    valign="middle",
                    text_size=(self.width - 20, None),
                )
                container.add_widget(item_lbl)

            os.makedirs("reports", exist_ok=True)
            self.pdf_path = gerar_relatorio_pdf(
                unidades=unidades,
                val_fixo=val_fixo,
                t_fixa=t_fixa,
                val_var=val_var,
                total_moro=total_moro,
                t_var=t_var,
                mes_ref=mes_ref,
            )

            self.ids.btn_download.disabled = False

        except (ValueError, OSError, RuntimeError) as ex:
            self._mostrar_erro(f"Erro ao processar cálculo/PDF: {ex}")

    def _mostrar_erro(self, mensagem: str) -> None:
        """Exibe erros e reabilita o botão."""
        container = self.ids.container_resultados
        container.clear_widgets()
        container.add_widget(
            Label(
                text=mensagem,
                color=(1, 0.2, 0.2, 1),
                size_hint_y=None,
                height=30,
            )
        )
        self.ids.btn_processar.disabled = False

    def baixar_pdf(self) -> None:
        """Abre o PDF gerado."""
        if self.pdf_path and os.path.exists(self.pdf_path):
            webbrowser.open(os.path.abspath(self.pdf_path))


class MeuApp(App):
    """Main application class for water bill distribution."""

    def build(self):
        # ... retorno da sua tela principal
        pass

if __name__ == '__main__':
    MeuApp().run()
