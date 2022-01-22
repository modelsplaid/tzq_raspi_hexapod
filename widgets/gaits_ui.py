# Widgets used to set the leg pose of all legs uniformly
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
import dash
import dash_daq
from texts import GAITS_WIDGETS_HEADER
from settings import (
    ALPHA_MAX_ANGLE,
    BETA_MAX_ANGLE,
    GAMMA_MAX_ANGLE,
    UPDATE_MODE,
    SLIDER_ANGLE_RESOLUTION,
)
from style_settings import SLIDER_THEME, SLIDER_HANDLE_COLOR, SLIDER_COLOR


def make_slider(slider_id, name, max_angle):

    handle_style = {
        "showCurrentValue": True,
        "color": SLIDER_HANDLE_COLOR,
        "label": name,
    }

    daq_slider = dash_daq.Slider(  # pylint: disable=not-callable
        id=slider_id,
        min=-max_angle,
        max=max_angle,
        value=7.5,
        step=SLIDER_ANGLE_RESOLUTION,
        size=300,
        updatemode=UPDATE_MODE,
        handleLabel=handle_style,
        color={"default": SLIDER_COLOR},
        theme=SLIDER_THEME,
    )
    testfont = dash.html.Font(name)
    
    return html.Div([testfont,daq_slider], style={"padding": "2%"})
    #return html.Div([testfont,daq_slider], style={"padding-top": "10%","padding-left": "5%"})


# ................................
# COMPONENTS
# ................................

HEADER = html.Label(dcc.Markdown(f"**{GAITS_WIDGETS_HEADER}**"))
WIDGET_NAMES = ["hipSwing", "liftSwing", "hipStance","liftStance","stepCount","speed"]
GAITS_WIDGET_IDS = [f"widget-{name}" for name in WIDGET_NAMES]
GAITS_CALLBACK_INPUTS = [Input(i, "value") for i in GAITS_WIDGET_IDS]

gaits_type_r_widges=dcc.RadioItems(
    options=[
        {'label': 'tripod gaits', 'value': 'tripod'},
        {'label': 'ripple gaits', 'value': 'ripple'},
    ],
    value='MTL',
    labelStyle={'display': 'inline-block'}, # display of flex to create a vertical list, or of inline-block for horizontal.
)

forward_backward_sel_r_widges=dcc.RadioItems(
    options=[
        {'label': 'moving forward', 'value': 'forward'},
        {'label': 'moving backward', 'value': 'backward'},
    ],
    value='MTL',
    labelStyle={'display': 'inline-block'}, # display of flex to create a vertical list, or of inline-block for horizontal.
)
walk_radio_widgets = [gaits_type_r_widges,forward_backward_sel_r_widges]

b1 = html.Button('Step by step', id='button1')
b2 = html.Button('Keep moving', id='button2')
steps_moving_b_widges = [b1,b2]

max_angles = [ALPHA_MAX_ANGLE, BETA_MAX_ANGLE, GAMMA_MAX_ANGLE,GAMMA_MAX_ANGLE,GAMMA_MAX_ANGLE,GAMMA_MAX_ANGLE]
widgets = [
    make_slider(id, name, angle)
    for id, name, angle in zip(GAITS_WIDGET_IDS, WIDGET_NAMES, max_angles)
]
GAITS_WIDGETS_SECTION = html.Div([HEADER] +steps_moving_b_widges  + walk_radio_widgets+ widgets)
