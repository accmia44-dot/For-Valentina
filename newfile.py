import random
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.core.text import Label as CoreLabel

# Color de fondo azul noche elegante
Window.clearcolor = (0.07, 0.09, 0.15, 1)

class BotonFijoCanvas(Button):
    """Botón blindado: Dibuja el texto como un gráfico en el canvas para que NUNCA se mueva o desaparezca"""
    def __init__(self, texto_fijo="", bg_color=(0.9, 0.3, 0.4, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.bg_color = bg_color
        self.texto_fijo = texto_fijo
        
        # Creamos una textura de texto fija e inamovible
        core_label = CoreLabel(text=self.texto_fijo, font_size=18, bold=True, color=(1, 1, 1, 1))
        core_label.refresh()
        self.text_texture = core_label.texture
        
        with self.canvas.before:
            # Color del botón
            self.color_grafico = Color(rgba=self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
            
            # Color del texto y su dibujo centrado
            Color(1, 1, 1, 1)
            self.rect_texto = RoundedRectangle(texture=self.text_texture, radius=[0])
        
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
        # Forzamos al texto a dibujarse exactamente en el centro del botón
        tw, th = self.text_texture.size
        cx = instance.x + (instance.width - tw) / 2
        cy = instance.y + (instance.height - th) / 2
        self.rect_texto.pos = (cx, cy)
        self.rect_texto.size = (tw, th)


class PantallaRomantica(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._reajustar_textos)
        self.mostrar_inicio()

    def limpiar(self):
        self.clear_widgets()

    def _reajustar_textos(self, instance, value):
        for child in self.children:
            if isinstance(child, Label) and not hasattr(child, 'es_flotante'):
                child.text_size = (instance.width * 0.9, None)

    def mostrar_inicio(self):
        self.limpiar()

        self.titulo = Label(
            text=(
                "Hola Valentina\n\n"
                "Hay algo que me gustaría preguntarte...\n\n"
                "¿Te gustaría volver a intentarlo?\n\n"
                "De una manera más madura,\n"
                "más tranquila\n"
                "y aprendiendo de nuestros errores."
            ),
            font_size="18sp",
            halign="center",
            valign="middle",
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            text_size=(Window.width * 0.9, None)
        )
        self.add_widget(self.titulo)

        # Usamos los nuevos botones blindados por Canvas
        self.boton_si = BotonFijoCanvas(
            texto_fijo="SÍ", 
            bg_color=(0.92, 0.23, 0.35, 1),
            size_hint=(0.35, 0.08),
            pos_hint={"center_x": 0.3, "center_y": 0.2}
        )

        self.boton_no = BotonFijoCanvas(
            texto_fijo="NO",
            bg_color=(0.25, 0.28, 0.36, 1),
            size_hint=(0.35, 0.08),
            pos_hint={"center_x": 0.7, "center_y": 0.2}
        )

        self.boton_si.bind(on_press=self.procesando_respuesta)
        self.boton_no.bind(on_press=self.mostrar_no)

        self.add_widget(self.boton_si)
        self.add_widget(self.boton_no)

        # Animación de latido en el botón SÍ
        anim = Animation(size_hint=(0.39, 0.09), duration=0.7, t='out_quad') + \
               Animation(size_hint=(0.35, 0.08), duration=0.7, t='in_quad')
        anim.repeat = True
        anim.start(self.boton_si)

    def procesando_respuesta(self, instance):
        self.limpiar()

        mensaje = Label(
            text="Procesando respuesta...\n\nPor favor espera...",
            font_size="22sp",
            halign="center",
            text_size=(Window.width * 0.9, None)
        )
        self.add_widget(mensaje)
        
        # Lluvia de corazones y palabras de fondo activa
        Clock.schedule_interval(self.generar_elemento_flotante, 0.4)
        Clock.schedule_once(self.iniciar_carga, 2)

    def generar_elemento_flotante(self, dt):
        palabras_bonitas = ["♥", "Te quiero", "Madurez", "Paz", "Tú y Yo", "Futuro", "Respeto", "Tranquilidad", "♥", "Perdón"]
        contenido = random.choice(palabras_bonitas)
        
        tamano = "24sp" if contenido == "♥" else "14sp"
        color_texto = (1, 0.3, 0.4, 0) if contenido == "♥" else (1, 1, 1, 0)

        label_flotante = Label(
            text=contenido,
            font_size=tamano,
            color=color_texto,
            size_hint=(None, None),
            pos=(random.randint(0, int(Window.width * 0.8)), random.randint(0, int(Window.height * 0.2)))
        )
        label_flotante.es_flotante = True
        
        self.add_widget(label_flotante, index=len(self.children))

        tiempo_vuelo = random.uniform(3.0, 5.0)
        altura_final = label_flotante.y + random.randint(350, 550)
        
        animacion = Animation(color=(color_texto[0], color_texto[1], color_texto[2], random.uniform(0.4, 0.7)), y=label_flotante.y + 100, duration=tiempo_vuelo*0.3) + \
                    Animation(color=(color_texto[0], color_texto[1], color_texto[2], 0), y=altura_final, duration=tiempo_vuelo*0.7)
        
        animacion.bind(on_complete=lambda anim, widget: self.remove_widget(widget))
        animacion.start(label_flotante)

    def iniciar_carga(self, dt):
        for child in list(self.children):
            if not hasattr(child, 'es_flotante'):
                self.remove_widget(child)
        
        self.porcentaje = 0

        self.label = Label(
            text="Iniciando sentimientos...\n\n0%",
            font_size="22sp",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            text_size=(Window.width * 0.9, None)
        )
        self.add_widget(self.label)

        self.barra = ProgressBar(
            max=100,
            value=0,
            size_hint=(0.75, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.45}
        )
        self.add_widget(self.barra)

        Clock.schedule_interval(self.actualizar_carga, 0.05)

    def actualizar_carga(self, dt):
        mensajes = [
            "Iniciando sentimientos...",
            "Recordando tu sonrisa...",
            "Pensando en nuestros momentos...",
            "Aprendiendo de los errores...",
            "Imaginando un nuevo comienzo...",
            "Preparando una mejor versión de mi...",
            "Pensando en Valentina...",
            "Cargando esperanza...",
            "Preparando una sorpresa...",
            "Oportunidad encontrada"
        ]

        if self.porcentaje < 100:
            self.porcentaje += 1
            self.barra.value = self.porcentaje
            indice = min(len(mensajes) - 1, self.porcentaje // 10)
            self.label.text = f"{mensajes[indice]}\n\n{self.porcentaje}%"
        else:
            Clock.unschedule(self.actualizar_carga)
            self.mostrar_oportunidad()

    def mostrar_oportunidad(self):
        for child in list(self.children):
            if not hasattr(child, 'es_flotante'):
                self.remove_widget(child)

        mensaje = Label(
            text=(
                "OPORTUNIDAD ENCONTRADA\n\n"
                "Analizando sentimientos...\n\n"
                "Persona detectada:\n"
                "Valentina\n\n"
                "Abriendo mensaje..."
            ),
            font_size="22sp",
            halign="center",
            text_size=(Window.width * 0.9, None)
        )
        self.add_widget(mensaje)
        Clock.schedule_once(lambda dt: self.mostrar_mensaje_final(), 2.5)

    def mostrar_mensaje_final(self):
        for child in list(self.children):
            if not hasattr(child, 'es_flotante'):
                self.remove_widget(child)

        mensaje = Label(
            text=(
                "VALENTINA\n\n"
                "Quizás el pasado no fue perfecto,\n"
                "ambos cometimos errores.\n\n"
                "Pero las mejores historias\n"
                "no son las que nunca fallan,\n"
                "son aquellas que aprenden,\n"
                "crecen y vuelven a intentarlo.\n\n"
                "No puedo cambiar el pasado,\n"
                "pero sí puedo aprender de él.\n\n"
                "Y si algún día decides\n"
                "dar una nueva oportunidad,\n"
                "me gustaría demostrarte\n"
                "que las cosas pueden ser diferentes.\n\n"
                "Sin presiones. Sin promesas vacías.\n"
                "Solo con sinceridad."
            ),
            font_size="16sp",
            halign="center",
            line_height=1.2,
            text_size=(Window.width * 0.9, None)
        )
        
        mensaje.color = (1, 1, 1, 0)
        self.add_widget(mensaje)
        anim = Animation(color=(1, 1, 1, 1), duration=2)
        anim.start(mensaje)

    def mostrar_no(self, instance):
        self.limpiar()

        mensaje = Label(
            text=(
                "Lo entiendo,\n"
                "no te preocupes corazón.\n\n"
                "Gracias por los momentos\n"
                "compartidos.\n\n"
                "Te deseo felicidad,\n"
                "tranquilidad\n"
                "y que te vaya bien en todo.\n\n"
                "Cuídate mucho."
            ),
            font_size="20sp",
            halign="center",
            text_size=(Window.width * 0.9, None)
        )
        self.add_widget(mensaje)
        Clock.schedule_once(self.cerrar_app, 6)

    def cerrar_app(self, dt):
        App.get_running_app().stop()


class AppRomantica(App):
    def build(self):
        self.title = "Para: Valentina"
        return PantallaRomantica()


if __name__ == "__main__":
    AppRomantica().run()
