Python 3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> # Update button
... @app.callback(
...     Output('flightnr_filter', 'value'),
...     Output('dest_filter', 'value'),
...     Output('slider-dep', 'value'),
...     Output('slider-lf', 'value'),
...     Output('dataSelection', 'value'),
...     Input('ResetButton', 'n_clicks'),
...     prevent_initial_call = True
...     )
... 
... def update_filters(value1):
...     flightfilter, destinations = None, None
...     slider1, slider2 = [0,23], [0,1]
...     radioItem = 'Shipments'
