import re
import math

float_re = re.compile(r'^([0-9]*[.]?[0-9]*).*')
parseFloat = lambda f: float(float_re.search(f).group(1))

rgb_hsl_re = re.compile(r'([a-z]+)\((.*)\)',re.IGNORECASE)

class Color(object):
    """Color object"""
    def __init__(self, color, opacity):
        """color is color format string; opacity is in [0,1]"""
        self.color = color
        self.opacity = opacity
    
    def brighter(k):
        pass
    
    def darker(k):
        pass

class Rgb(Color):
    """Class to hold RGB color objects"""
    def __init__(self, r, g, b, a=1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        
        color = "rgb(%i,%i,%i)" % (r,g,b)
        opacity = a
        Color.__init__(color,opacity)
        
        return self
    
    def red(self,r):
        return Rgb(r,self.g,self.b,self.a)
    
    def green(self,g):
        return Rgb(self.r,g,self.b,self.a)
    
    def blue(self,b):
        return Rgb(self.r,self.g,b,self.a)
    
    def alpha(self,a):
        return Rgb(self.r,self.g,self.b,a)
    
    def rgb(self):
        return self
    
    def brighter(self,k=1):
        k = 0.7 ** k
        r = self.r
        g = self.g
        b = self.b
        i = 30
        if r==0 and g==0 and b==0: return Rgb(i,i,i,self.a)
        if r > 0 and r < i: r = i
        if g > 0 and g < i: g = i
        if b > 0 and b < i: b = i
        return Rgb(min(255, math.floor(r/k)),
                   min(255, math.floor(g/k)),
                   min(255, math.floor(b/k)),
                   self.a)
    
    def darker(k=1):
        k = 0.7 ** k
        return Rgb(max(0, math.floor(k*self.r)),
                   max(0, math.floor(k*self.g)),
                   max(0, math.floor(k*self.b)),
                   self.a)

transparent = Rgb(0,0,0,0)



class Hsl(Color):
    """Class to hold HSL color objects"""
    def __init__(self, h, s, l, a=1):
        self.h = h
        self.s = s
        self.l = l
        self.a = a
        
        color = "hsl(%i,%f%%,%f%%)" % (h,s*100,l*100)
        opacity = a
        Color.__init__(color,opacity)
        
        return self
    
    def hue(h):
        return Hsl(h,self.s,self.l,self.a)
    
    def saturation(s):
        return Hsl(self.h,s,self.l,self.a)
        
    def lightness(h):
        return Hsl(self.h,self.s,l,self.a)
        
    def alpha(h):
        return Hsl(self.h,self.s,self.l,a)
    
    def rgb(self):
        """Returns Rgb version of self"""
        h = self.h
        s = self.s
        l = self.l
        
        # some corrections
        h = h % 360
        if h < 0: h += 360
        
        s = max(0, min(s, 1))
        
        l = max(0, min(s, 1))
        
        # from FvD 13.37, CSS Color Module Level 3
        m2 = (l*(1+s)) if (l <= 0.5) else (l+s-l*s)
        m1 = 2 * l - m2
        
        def v(h):
            if h > 360:
                h -= 360
            elif h < 0:
                h += 360
            if h < 60:  return m1 + (m2 - m1) * h / 60
            if h < 180: return m2
            if h < 240: return m1 + (m2 - m1) * (240 - h) / 60
            return m1
        
        def vv(h):
            return round(v(h) * 255)
        
        return Rgb(vv(h+120), vv(h), vv(h-120), self.a)



def color(format):
    """Parses color specs and returns Rgb object."""
    if isinstance(format,Rgb):
        return format
    
    # HSL or RGB specs (e.g., rgba(12,43,65))
    try:
        (space,values_string) = rgb_hsl_re.search(format).group(1,2)
        raw_values = values_string.split(',')
        if len(raw_values) != 3 or len(raw_values) != 4:
            raise ValueError, "expected 3 or 4 values for RGB(A)/HSL(A) string"
        
        # determine the alpha value
        a = 1
        if space == 'hsla' or space == 'rgba':
            a = parseFloat(raw_values[3])
            if a == 0.:
                return transparent
        
        if space == 'hsla' or space == 'hsl':
            h = parseFloat(raw_values[0])    # degrees
            s = parseFloat(raw_values[1]) / 100.    # percentage
            l = parseFloat(raw_values[2]) / 100.    # percentage
            return Hsl(h,s,l,a).rgb()
        
        if space == 'rgba' or space == 'rgb':
            r = parseFloat(raw_values[0])
            g = parseFloat(raw_values[1])
            b = parseFloat(raw_values[2])
            if raw_values[0][-1] == '%': r = r / 100.
            if raw_values[1][-1] == '%': g = g / 100.
            if raw_values[2][-1] == '%': b = b / 100.
            return Rgb(r,g,b,a)
    except AttributeError:
        pass
    
    # Try a named color instead
    try:
        named = names[format]
        return named
    except KeyError:
        pass
    
    # Try a hexadecimal color: #rgb or #rrggbb
    if format[0] == '#':
        if len(format) == 4:
            r = format[1]
            g = format[2]
            b = format[3]
        elif len(format) == 7:
            r = format[1:3]
            g = format[3:5]
            b = format[5:7]
        else:
            raise ValueError, "hex strings should be formatted as '#rgb' or '#rrggbb'"
        return Rgb(int(r,16),int(g,16),int(b,16))
    
    # Something else. pass-through unsupported colors
    return Color(format,1)

names = {
    "aliceblue":"#f0f8ff",
    "antiquewhite":"#faebd7",
    "aqua":"#00ffff",
    "aquamarine":"#7fffd4",
    "azure":"#f0ffff",
    "beige":"#f5f5dc",
    "bisque":"#ffe4c4",
    "black":"#000000",
    "blanchedalmond":"#ffebcd",
    "blue":"#0000ff",
    "blueviolet":"#8a2be2",
    "brown":"#a52a2a",
    "burlywood":"#deb887",
    "cadetblue":"#5f9ea0",
    "chartreuse":"#7fff00",
    "chocolate":"#d2691e",
    "coral":"#ff7f50",
    "cornflowerblue":"#6495ed",
    "cornsilk":"#fff8dc",
    "crimson":"#dc143c",
    "cyan":"#00ffff",
    "darkblue":"#00008b",
    "darkcyan":"#008b8b",
    "darkgoldenrod":"#b8860b",
    "darkgray":"#a9a9a9",
    "darkgreen":"#006400",
    "darkgrey":"#a9a9a9",
    "darkkhaki":"#bdb76b",
    "darkmagenta":"#8b008b",
    "darkolivegreen":"#556b2f",
    "darkorange":"#ff8c00",
    "darkorchid":"#9932cc",
    "darkred":"#8b0000",
    "darksalmon":"#e9967a",
    "darkseagreen":"#8fbc8f",
    "darkslateblue":"#483d8b",
    "darkslategray":"#2f4f4f",
    "darkslategrey":"#2f4f4f",
    "darkturquoise":"#00ced1",
    "darkviolet":"#9400d3",
    "deeppink":"#ff1493",
    "deepskyblue":"#00bfff",
    "dimgray":"#696969",
    "dimgrey":"#696969",
    "dodgerblue":"#1e90ff",
    "firebrick":"#b22222",
    "floralwhite":"#fffaf0",
    "forestgreen":"#228b22",
    "fuchsia":"#ff00ff",
    "gainsboro":"#dcdcdc",
    "ghostwhite":"#f8f8ff",
    "gold":"#ffd700",
    "goldenrod":"#daa520",
    "gray":"#808080",
    "green":"#008000",
    "greenyellow":"#adff2f",
    "grey":"#808080",
    "honeydew":"#f0fff0",
    "hotpink":"#ff69b4",
    "indianred":"#cd5c5c",
    "indigo":"#4b0082",
    "ivory":"#fffff0",
    "khaki":"#f0e68c",
    "lavender":"#e6e6fa",
    "lavenderblush":"#fff0f5",
    "lawngreen":"#7cfc00",
    "lemonchiffon":"#fffacd",
    "lightblue":"#add8e6",
    "lightcoral":"#f08080",
    "lightcyan":"#e0ffff",
    "lightgoldenrodyellow":"#fafad2",
    "lightgray":"#d3d3d3",
    "lightgreen":"#90ee90",
    "lightgrey":"#d3d3d3",
    "lightpink":"#ffb6c1",
    "lightsalmon":"#ffa07a",
    "lightseagreen":"#20b2aa",
    "lightskyblue":"#87cefa",
    "lightslategray":"#778899",
    "lightslategrey":"#778899",
    "lightsteelblue":"#b0c4de",
    "lightyellow":"#ffffe0",
    "lime":"#00ff00",
    "limegreen":"#32cd32",
    "linen":"#faf0e6",
    "magenta":"#ff00ff",
    "maroon":"#800000",
    "mediumaquamarine":"#66cdaa",
    "mediumblue":"#0000cd",
    "mediumorchid":"#ba55d3",
    "mediumpurple":"#9370db",
    "mediumseagreen":"#3cb371",
    "mediumslateblue":"#7b68ee",
    "mediumspringgreen":"#00fa9a",
    "mediumturquoise":"#48d1cc",
    "mediumvioletred":"#c71585",
    "midnightblue":"#191970",
    "mintcream":"#f5fffa",
    "mistyrose":"#ffe4e1",
    "moccasin":"#ffe4b5",
    "navajowhite":"#ffdead",
    "navy":"#000080",
    "oldlace":"#fdf5e6",
    "olive":"#808000",
    "olivedrab":"#6b8e23",
    "orange":"#ffa500",
    "orangered":"#ff4500",
    "orchid":"#da70d6",
    "palegoldenrod":"#eee8aa",
    "palegreen":"#98fb98",
    "paleturquoise":"#afeeee",
    "palevioletred":"#db7093",
    "papayawhip":"#ffefd5",
    "peachpuff":"#ffdab9",
    "peru":"#cd853f",
    "pink":"#ffc0cb",
    "plum":"#dda0dd",
    "powderblue":"#b0e0e6",
    "purple":"#800080",
    "red":"#ff0000",
    "rosybrown":"#bc8f8f",
    "royalblue":"#4169e1",
    "saddlebrown":"#8b4513",
    "salmon":"#fa8072",
    "sandybrown":"#f4a460",
    "seagreen":"#2e8b57",
    "seashell":"#fff5ee",
    "sienna":"#a0522d",
    "silver":"#c0c0c0",
    "skyblue":"#87ceeb",
    "slateblue":"#6a5acd",
    "slategray":"#708090",
    "slategrey":"#708090",
    "snow":"#fffafa",
    "springgreen":"#00ff7f",
    "steelblue":"#4682b4",
    "tan":"#d2b48c",
    "teal":"#008080",
    "thistle":"#d8bfd8",
    "tomato":"#ff6347",
    "turquoise":"#40e0d0",
    "violet":"#ee82ee",
    "wheat":"#f5deb3",
    "white":"#ffffff",
    "whitesmoke":"#f5f5f5",
    "yellow":"#ffff00",
    "yellowgreen":"#9acd32",
    "transparent": transparent
}

for name in names.iterkeys():
    names[name] = color(names[name])






