# cnftsniper
cNFT Sniper / monitoring app built with Streamlit and python3. Currently this app monitors listings on jpg.store and refreshes based on a user defined interval. The app is capable of filtering results based on traits.

__Alpha:__

This is an initial version and is in no way intended for use in a production environment. Bugs and issues likely exist, and all concepts have not been fully developed. This version is intended to act as a skeleton / framework to be used for further collaboration / experimentation. Code is very rudimentary at this point.

__Stop:__

Please note, the stop button is not always 100% immediate. Sometimes need to wait a sec or click a second time.

__jpg.store:__

The currently supplied api only supports usage with jpg.store. Api's for other marketplaces need to be developed.

__Requirements:__
```
bs4
natsort
requests
streamlit
```

__Usage:__

`streamlit run sniper.py`
