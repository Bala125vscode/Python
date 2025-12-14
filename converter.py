import re
from app.units import UNIT_MAP

class LatexConverter:
    def __init__(self):
        # Compile regex for unit mapping
        sorted_keys = sorted(UNIT_MAP.keys(), key=len, reverse=True)
        patterns = []
        for key in sorted_keys:
            esc = re.escape(key)
            # If key is like \word (letters only), add boundary check
            # to prevent \m matching start of \meter or \text
            if re.match(r"\\[a-zA-Z]+$", key):
                patterns.append(esc + r"(?![a-zA-Z])")
            else:
                patterns.append(esc)
        
        self.unit_pattern = re.compile('|'.join(patterns))

    def _tokenize_unit(self, unit_str):
        """
        Tokenizes unit string into commands and text.
        Returns list of (type, value) tuples.
        types: 'CMD', 'TEXT', 'ARG'
        """
        tokens = []
        i = 0
        n = len(unit_str)
        while i < n:
            char = unit_str[i]
            if char == '\\':
                j = i + 1
                while j < n and unit_str[j].isalpha():
                    j += 1
                cmd = unit_str[i:j]
                tokens.append(('CMD', cmd))
                i = j
                # Check for argument immediately for specific commands?
                # Actually, better to parse args as separate tokens or attached.
                # Let's do simple tokenization first.
            elif char == '{':
                # Extract braced content as ARG
                arg, end = self._extract_braced_content(unit_str, i)
                if arg is not None:
                    tokens.append(('ARG', arg))
                    i = end + 1
                else:
                    tokens.append(('TEXT', char))
                    i += 1
            elif char.isspace():
                i += 1
            else:
                tokens.append(('TEXT', char))
                i += 1
        return tokens

    def _map_unit(self, unit_str):
        """
        Maps siunitx unit macros to standard LaTeX text commands.
        Handles modifiers: \\per, \\square, \\cubic, \\tothe, \\raiseto.
        """
        # Direct lookup if simple
        if unit_str in UNIT_MAP:
            return UNIT_MAP[unit_str]

        tokens = self._tokenize_unit(unit_str)
        output = []
        
        # State
        sign = 1
        next_power = None # From \raiseto, \square, \cubic
        
        i = 0
        while i < len(tokens):
            typ, val = tokens[i]
            consumed = False
            
            if typ == 'CMD':
                if val == '\\per':
                    sign = -1
                    consumed = True
                elif val == '\\square':
                    next_power = 2
                    consumed = True
                elif val == '\\cubic':
                    next_power = 3
                    consumed = True
                elif val == '\\raiseto':
                    # Expect ARG
                    if i + 1 < len(tokens) and tokens[i+1][0] == 'ARG':
                        next_power = tokens[i+1][1]
                        i += 1 # Skip arg
                    consumed = True
                elif val in UNIT_MAP:
                    # It's a unit
                    mapped = UNIT_MAP[val]
                    
                    # Determine base power from prefixes
                    p = 1
                    if next_power is not None:
                        p = next_power
                        next_power = None
                    
                    # Lookahead for suffixes: \tothe, \squared, \cubed
                    # These override or modify p? usually set it.
                    j = i + 1
                    suffix_power = None
                    while j < len(tokens):
                        styp, sval = tokens[j]
                        if styp == 'CMD':
                            if sval == '\\tothe':
                                if j + 1 < len(tokens) and tokens[j+1][0] == 'ARG':
                                    suffix_power = tokens[j+1][1]
                                    j += 1 # consume arg
                                j += 1 # consume cmd
                                i = j - 1 # Update main loop index (it will increment at end)
                                continue # Keep looking? \tothe usually last?
                            elif sval == '\\squared':
                                suffix_power = 2
                                j += 1
                                i = j - 1
                                continue
                            elif sval == '\\cubed':
                                suffix_power = 3
                                j += 1
                                i = j - 1
                                continue
                        break
                    
                    if suffix_power is not None:
                        # Suffix wins over prefix power (e.g. \square\meter\cubed -> M^3? Ambiguous, assume suffix)
                        p = suffix_power
                    
                    # Calculate final exponent
                    # sign only applies if we had \per
                    
                    exponent = ""
                    # Logic: if sign is -1, result is -p
                    
                    # Check if p is a number
                    try:
                        fp = float(p)
                        total = fp * sign
                        # Format nicely
                        if total != 1: # standard unit has checking
                             if total == int(total):
                                 total_str = str(int(total))
                             else:
                                 total_str = str(total)
                             
                             exponent = f"^{{{total_str}}}"
                    except ValueError:
                        # p is a string variable
                        if sign == -1:
                            exponent = f"^{{-{p}}}"
                        else:
                            exponent = f"^{{{p}}}"
                    
                    output.append(f"{mapped}{exponent}")
                    sign = 1
                    consumed = True
                
                # If command handled, continue
                if consumed:
                    i += 1
                    continue
                
                # Unknown command
                output.append(val)
                
            elif typ == 'TEXT':
                output.append(val)
            elif typ == 'ARG':
                # Unexpected arg
                pass
            
            i += 1
            
        return "".join(output)
    def _extract_braced_content(self, text, start_index):
        """
        Extracts content inside nested braces starting from start_index.
        Returns (content, end_index) where end_index is the index of the closing brace.
        Returns (None, -1) if no valid braced content is found.
        """
        if start_index >= len(text) or text[start_index] != '{':
            return None, -1

        balance = 0
        for i in range(start_index, len(text)):
            char = text[i]
            if char == '{':
                balance += 1
            elif char == '}':
                balance -= 1
                if balance == 0:
                    return text[start_index+1:i], i
        return None, -1

    def _extract_optional_arg(self, text, start_index):
        """
        Extracts content inside optional brackets [...] starting from start_index.
        Returns (content, end_index) where end_index is the index of the closing bracket.
        Returns (None, start_index) if the next char is not [.
        """
        # Skip whitespace? Standard LaTeX usually allows whitespace before arguments but let's be strict for now or look ahead.
        # Simple lookahead for [
        i = start_index
        while i < len(text) and text[i].isspace():
            i += 1
        
        if i >= len(text) or text[i] != '[':
            return None, start_index # No optional arg, return original start_index (shifted if whitespace)

        balance = 0
        for j in range(i, len(text)):
            char = text[j]
            if char == '[':
                balance += 1
            elif char == ']':
                balance -= 1
                if balance == 0:
                    return text[i+1:j], j
        return None, start_index

    def _parse_number(self, num_str):
        """
        Basic parsing of \\num{...} content to standard LaTeX.
        Handles e-notation and uncertainties.
        """
        # Handle +/- or +- -> \pm
        num_str = num_str.replace('+/-', '\\pm ').replace('+-', '\\pm ')
        
        # Handle e-notation: 1.23e4 -> 1.23 \times 10^{4}
        # Regex looks for 'e' or 'E' preceded by a digit or dot, and followed by integer.
        match = re.search(r'(?<=[\d\.])[eE]([+-]?\d+)\b', num_str)
        if match:
            exp = match.group(1)
            base = num_str[:match.start()]
            return f"{base} \\times 10^{{{exp}}}"
        
        return num_str


    def _parse_complex(self, content):
        """
        Handles \\complexnum{...}.
        Example: 1+-2i -> 1+-2\\mathrm{i}
        """
        # Replace i or j at the end of a number or standalone with \mathrm{i} or \mathrm{j}
        content = re.sub(r'(?<!\\)(\d+|\b)[ij]\b', r'\1\\mathrm{i}', content)
        
        # Handle polar form: 10 \angle 30 -> 10 \angle 30^{\circ}
        if r'\angle' in content:
            # Assume format mag \angle phase
            parts = content.split(r'\angle')
            if len(parts) == 2:
                mag = self._parse_number(parts[0].strip())
                phase = self._parse_number(parts[1].strip())
                return f"{mag} \\angle {phase}^{{\\circ}}"

        # Handle polar with : (10:30) used in some contexts? 
        # siunitx usually uses \angle or just typed input.
        
        return self._parse_number(content)

    def _parse_list(self, content, unit=None):
        """
        Handles \\numlist{1;2;3} -> 1, 2 and 3
        """
        items = content.split(';')
        parsed_items = [self._parse_number(item.strip()) for item in items]
        
        if len(parsed_items) == 0:
            return ""
        
        res = ""
        if len(parsed_items) == 1:
            res = parsed_items[0]
        elif len(parsed_items) == 2:
            res = f"{parsed_items[0]} \\text{{ and }} {parsed_items[1]}"
        else:
            res = ", ".join(parsed_items[:-1]) + f" \\text{{ and }} {parsed_items[-1]}"
            
        if unit:
            res += f"\\,{self._map_unit(unit)}"
            
        return res

    def _parse_product(self, content, unit=None):
        """
        Handles \\numproduct{1 x 2 x 3} -> 1 \\times 2 \\times 3
        """
        items = content.split('x')
        parsed_items = [self._parse_number(item.strip()) for item in items]
        res = " \\times ".join(parsed_items)
        if unit:
            res += f"\\,{self._map_unit(unit)}"
        return res

    def _parse_range(self, num1, num2, unit=None):
        """
        Handles \\numrange{1}{10} -> 1 -- 10
        """
        n1 = self._parse_number(num1)
        n2 = self._parse_number(num2)
        res = f"{n1} \\text{{--}} {n2}"
        if unit:
            res += f"\\,{self._map_unit(unit)}"
        return res

    def convert(self, text):
        output = []
        i = 0
        n = len(text)
        
        while i < n:
            if text[i] == '\\':
                # Identify command
                j = i + 1
                while j < n and text[j].isalpha():
                    j += 1
                cmd = text[i:j]
                
                # Logic for SIUNITX
                if cmd == '\\num':
                    arg, end = self._extract_braced_content(text, j)
                    if arg is not None:
                        output.append(self._parse_number(arg))
                        i = end + 1
                        continue
                
                elif cmd == '\\complexnum':
                    arg, end = self._extract_braced_content(text, j)
                    if arg is not None:
                        output.append(self._parse_complex(arg))
                        i = end + 1
                        continue
                        
                elif cmd in ['\\unit', '\\si']:
                    # Handle optional arg [per-mode=symbol]
                    _, opt_end = self._extract_optional_arg(text, j)
                    
                    arg, end = self._extract_braced_content(text, opt_end + 1 if opt_end != j else j)
                    if arg is not None:
                        output.append(self._map_unit(arg))
                        i = end + 1
                        continue

                elif cmd in ['\\qty', '\\SI']:
                    # \qty[opts]{num}{unit}
                    _, opt_end = self._extract_optional_arg(text, j)
                    
                    num_arg, end1 = self._extract_braced_content(text, opt_end + 1 if opt_end != j else j)
                    if num_arg is not None:
                        # Check for second arg
                        unit_arg, end2 = self._extract_braced_content(text, end1 + 1)
                        if unit_arg is not None:
                            output.append(f"{self._parse_number(num_arg)}\\,{self._map_unit(unit_arg)}")
                            i = end2 + 1
                            continue

                elif cmd in ['\\numlist', '\\numproduct']:
                    _, opt_end = self._extract_optional_arg(text, j)
                    arg, end = self._extract_braced_content(text, opt_end + 1 if opt_end != j else j)
                    if arg is not None:
                        if cmd == '\\numlist':
                            output.append(self._parse_list(arg))
                        else:
                            output.append(self._parse_product(arg))
                        i = end + 1
                        continue

                elif cmd in ['\\qtylist', '\\qtyproduct']:
                    _, opt_end = self._extract_optional_arg(text, j)
                    arg1, end1 = self._extract_braced_content(text, opt_end + 1 if opt_end != j else j)
                    if arg1 is not None:
                        arg2, end2 = self._extract_braced_content(text, end1 + 1)
                        if arg2 is not None:
                            if cmd == '\\qtylist':
                                output.append(self._parse_list(arg1, unit=arg2))
                            else:
                                output.append(self._parse_product(arg1, unit=arg2))
                            i = end2 + 1
                            continue

                elif cmd in ['\\numrange', '\\SIrange', '\\qtyrange']:
                    _, opt_end = self._extract_optional_arg(text, j)
                    arg1, end1 = self._extract_braced_content(text, opt_end + 1 if opt_end != j else j)
                    if arg1 is not None:
                        arg2, end2 = self._extract_braced_content(text, end1 + 1)
                        if arg2 is not None:
                            if cmd == '\\numrange':
                                output.append(self._parse_range(arg1, arg2))
                                i = end2 + 1
                                continue
                            else: # qtyrange, SIrange requires 3rd arg for unit?
                                # \qtyrange{1}{10}{\meter}
                                arg3, end3 = self._extract_braced_content(text, end2 + 1)
                                if arg3 is not None:
                                    output.append(self._parse_range(arg1, arg2, unit=arg3))
                                    i = end3 + 1
                                    continue
                        # Fallback if args missing? 
                        
                elif cmd == '\\ang':
                    arg, end = self._extract_braced_content(text, j)
                    if arg is not None:
                        if ';' in arg:
                            parts = arg.split(';')
                            # parts[0] is degrees, parts[1] is minutes, parts[2] is seconds
                            res = ""
                            if parts[0].strip():
                                res += f"{parts[0]}^{{\\circ}}"
                            if len(parts) > 1 and parts[1].strip():
                                res += f"{parts[1]}'"
                            if len(parts) > 2 and parts[2].strip():
                                res += f"{parts[2]}''"
                            output.append(res)
                        else:
                            output.append(f"{arg}^{{\\circ}}")
                        i = end + 1
                        continue

                # Tabular Column Types (S -> c)
                # This is a naive replacement for \begin{tabular}{...S...}
                # We need to detect \begin{tabular} and then modify its argument.
                elif cmd == '\\begin':
                    arg, end = self._extract_braced_content(text, j)
                    if arg == 'tabular':
                        output.append('\\begin{tabular}')
                        # The next braced group is the column spec
                        spec, end_spec = self._extract_braced_content(text, end + 1)
                        if spec is not None:
                            # Replace S with c (centering is a safe default for numbers)
                            new_spec = spec.replace('S', 'c')
                            output.append(f"{{{new_spec}}}")
                            i = end_spec + 1
                            continue
                        else:
                            i = end + 1
                            continue
                    else:
                        output.append(f"\\begin{{{arg}}}")
                        i = end + 1
                        continue

                # Logic for PHYSICS
                # Derivatives: \dv{x}, \dv{f}{x}, \dv[n]{f}{x}
                elif cmd == '\\dv':
                    opt_arg, opt_end = self._extract_optional_arg(text, j)
                    arg1, end1 = self._extract_braced_content(text, opt_end + 1 if opt_end != j else j)
                    
                    if arg1 is not None:
                        # Check for second arg
                        arg2, end2 = self._extract_braced_content(text, end1 + 1)
                        if arg2 is not None:
                            # \dv{f}{x} -> \frac{d f}{d x}
                            order = f"^{opt_arg}" if opt_arg else ""
                            output.append(f"\\frac{{\\mathrm{{d}}{order} {arg1}}}{{\\mathrm{{d}}{arg2}{order}}}")
                            i = end2 + 1
                        else:
                            # \dv{x} -> \mathrm{d}x (differentials?) usually \dd is differential, \dv is derivative
                            # But \dv{x} sometimes means d/dx operator if single arg? 
                            # Physics package doc: \dv{x} -> d/dx. \dv{f}{x} -> df/dx.
                            order = f"^{opt_arg}" if opt_arg else ""
                            output.append(f"\\frac{{\\mathrm{{d}}{order}}}{{\\mathrm{{d}}{arg1}{order}}}")
                            i = end1 + 1
                        continue

                elif cmd == '\\pdv':
                    opt_arg, opt_end = self._extract_optional_arg(text, j)
                    arg1, end1 = self._extract_braced_content(text, opt_end + 1 if opt_end != j else j)
                    
                    if arg1 is not None:
                        arg2, end2 = self._extract_braced_content(text, end1 + 1)
                        if arg2 is not None:
                             # \pdv{f}{x}
                            order = f"^{opt_arg}" if opt_arg else ""
                            output.append(f"\\frac{{\\partial{order} {arg1}}}{{\\partial {arg2}{order}}}")
                            i = end2 + 1
                        else:
                            # \pdv{x} -> partial/partial x
                            order = f"^{opt_arg}" if opt_arg else ""
                            output.append(f"\\frac{{\\partial{order}}}{{\\partial {arg1}{order}}}")
                            i = end1 + 1
                        continue

                # Bracy things: \abs, \norm
                elif cmd == '\\abs':
                    arg, end = self._extract_braced_content(text, j)
                    if arg is not None:
                        output.append(f"\\left| {arg} \\right|")
                        i = end + 1
                        continue
                elif cmd == '\\norm':
                    arg, end = self._extract_braced_content(text, j)
                    if arg is not None:
                        output.append(f"\\left\\| {arg} \\right\\|")
                        i = end + 1
                        continue
                
                # Vectors
                elif cmd == '\\vb':
                    arg, end = self._extract_braced_content(text, j)
                    if arg is not None:
                        output.append(f"\\mathbf{{{arg}}}")
                        i = end + 1
                        continue
                
                # Bras and Kets
                elif cmd == '\\bra':
                    arg, end = self._extract_braced_content(text, j)
                    if arg is not None:
                        output.append(f"\\langle {arg} |")
                        i = end + 1
                        continue
                elif cmd == '\\ket':
                    arg, end = self._extract_braced_content(text, j)
                    if arg is not None:
                        output.append(f"| {arg} \\rangle")
                        i = end + 1
                        continue
                elif cmd == '\\braket':
                    arg1, end1 = self._extract_braced_content(text, j)
                    if arg1 is not None:
                        arg2, end2 = self._extract_braced_content(text, end1 + 1)
                        if arg2 is not None:
                            output.append(f"\\langle {arg1} | {arg2} \\rangle")
                            i = end2 + 1
                        else:
                             # \braket{x} -> <x|x> usually? Or just <x|
                             # Physics package: \braket{a} -> <a|a> NO, \braket{a} -> <a| 
                             # Wait, \braket{a}{b} is <a|b>. \braket{a} is usually just inner product placeholder?
                             # Let's assume 2 args for standard usage, if 1 arg, maybe it is <a|a> check docs.
                             # Docs say: \braket{a} -> <a|a>.
                             output.append(f"\\langle {arg1} | {arg1} \\rangle")
                             i = end1 + 1
                        continue

                # If no match, just append the command extraction
                output.append(cmd)
                i = j
            else:
                output.append(text[i])
                i += 1
        
        return "".join(output)
