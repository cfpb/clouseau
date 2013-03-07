# -*- coding: utf-8 -*-
# Original source liberally refactored.



prefix = "\033["

codes = {
    "reset"       : prefix + "0m",         
    "bold"        : prefix + "1m", 
    "italic"      : prefix + "3m",  # Generally not supported
    "strike"      : prefix + "09m", # Ibid
    "gray"        : prefix + "1;30m",
    "black"       : prefix + "30m",
    "red"         : prefix + "1;31m",
    "darkred"     : prefix + "31m",
    "green"       : prefix + "1;32m",
    "darkgreen"   : prefix + "32m",
    "yellow"      : prefix + "1;33m",
    "brown"       : prefix + "33m",
    "blue"        : prefix + "1;34m",
    "darkblue"    : prefix + "34m",
    "fuscia"      : prefix + "1;35m",
    "purple"      : prefix + "35m",
    "cyan"        : prefix + "1;36m",
    "darkcyan"    : prefix + "36m",
    "white"       : prefix + "1;37m",
    "smoke"       : prefix + "37m",
    "default"     : prefix + "39m",
    #Add soe BG Colors
    "yellow_bg"   : prefix + "43m",
    "cyan_bg"     : prefix + "46m",
    "blue_bg"     : prefix + "42m",
    "orange_bg"   : prefix + "41m",
    "white_bg"    : prefix + "47m",
    "default_bg"  : prefix + "49m"
}



symbols = {
  'ok'  : '✓',
  'fail'  : '✖',
  'dot' : '.',
  'em_dash': '—'
}



# --- main ---
def reset():
	return codes["reset"]

def color( _color, text ):
	return ("%s%s%s" % (codes[_color], text, codes["reset"]) )



# ---- Test output functions ----
def ok( text='' ):
    return ("%s %s" % (green( symbols['ok'] ), text) )

def fail( text='' ):
    return red( symbols['fail'] ) + ' ' + text

def em_dash():
    return symbols['em_dash'] 


# ---- Background colors as function calls ---:
def cyan_bg( text ):
    return color( 'cyan_bg', text )


def blue_bg( text ):
    return  color( 'blue_bg', text )

def orange_bg( text ):
    return color( 'orange_bg', text )

def white_bg( text ):
    return color( 'white_bg', text )

def default_bg( text ):
    return color( 'default_bg', text )


#
# ---- Colors wrapped in function calls ------:
#

def default( text ):
    return color( 'default', text )

def black( text ):
    return color( 'black', text )

def bold( text ):
	return color( 'bold', text )

def white( text ):
	return color( 'white', text )

def smoke( text ):
    return color( 'smoke', text )

def darkcyan( text ):
	return color( "darkcyan" , text )

def cyan( text ):
	return color( 'cyan', text )

def fuscia( text ):
	return color( 'fuscia' , text )

def purple( text ):
	return color( 'purple' , text )

def blue( text ):
	return color( 'blue', text )

def darkblue( text ):
	return color( 'darkblue', text )

def green( text ):
	return color( 'green', text )

def darkgreen( text ):
	return color( 'darkgreen', text )

def yellow( text ):
	return color( 'yellow', text )

def brown( text ):
	return color( 'brown', text )

def red( text ):
	return color( 'red', text )

def darkred( text ):
	return color( 'darkred', text )

def cyan( text ):
    return color( 'cyan', text)

def gray( text ):
    return color( 'gray', text )
