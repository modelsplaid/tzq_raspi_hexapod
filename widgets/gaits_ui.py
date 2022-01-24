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


def make_radio(radio_id, label_name, value):

    dcc.RadioItems(
        options=[
            {'label': 'moving forward', 'value': 'forward'},
            {'label': 'moving backward', 'value': 'backward'},
        ],
        value='MTL',
        labelStyle={'display': 'inline-block'}, # display of flex to create a vertical list, or of inline-block for horizontal.
    )


def make_button(button_id, button_name):
    return html.Button(button_name, id=button_id)

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

# 1 make sliders widgets
WIDGET_NAMES = ["hipSwing", "liftSwing", "hipStance","liftStance","stepCount","speed"]
GAITS_WIDGET_IDS = [f"widget-{name}" for name in WIDGET_NAMES]
GAITS_CALLBACK_INPUTS = [Input(i, "value") for i in GAITS_WIDGET_IDS]

max_angles = [ALPHA_MAX_ANGLE, BETA_MAX_ANGLE, GAMMA_MAX_ANGLE,GAMMA_MAX_ANGLE,GAMMA_MAX_ANGLE,GAMMA_MAX_ANGLE]
widgets = [
    make_slider(id, name, angle)
    for id, name, angle in zip(GAITS_WIDGET_IDS, WIDGET_NAMES, max_angles)
]

# 2. make button widgets
BUTTON_NAMES = ['Step by step','Keep moving']
BUTTON_IDS = [f"button-widget-{name}" for name in BUTTON_NAMES]
button_widgets = [
    make_button(id,name)
    for id,name in zip(BUTTON_IDS,BUTTON_NAMES)

]

# 3. make radio widgets
RADIO_NAMES = ['Gait types','Moving directions']
RADIO_IDS = [f"radio-widget-{name}" for name in RADIO_NAMES]

RADIO_OPTIONS_GAIT_TYPE_LABELS = ['tripod gaits','ripple gaits']
RADIO_OPTIONS_GAIT_TYPE_VALUES = ['tripod','ripple']

RADIO_OPTIONS_MOVING_DIRS_LABELS = ['moving forward','moving backward']
RADIO_OPTIONS_MOVING_DIR_VALUES = ['forward','backward']

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


GAITS_WIDGETS_SECTION = html.Div([HEADER] +button_widgets + walk_radio_widgets+ widgets)
