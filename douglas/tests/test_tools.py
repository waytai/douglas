# -*- coding: utf-8 -*-
import string
import os
import os.path

from douglas import app, tools
from douglas.tests import UnitTestBase


req = app.Request({}, {}, {})

 
class Testis_year(UnitTestBase):
    """tools.is_year"""
    def test_must_be_four_digits(self):
        for mem in (("abab", 0),
                    ("ab", 0),
                    ("199", 0),
                    ("19999", 0),
                    ("1997", 1),
                    ("2097", 1)):
            self.eq_(tools.is_year(mem[0]), mem[1])

    def test_must_start_with_19_or_20(self):
        for mem in (("3090", 0),
                    ("0101", 0)):
            self.eq_(tools.is_year(mem[0]), mem[1])

    def test_everything_else_returns_false(self):
        for mem in ((None, 0),
                    ("", 0),
                    ("ab", 0),
                    ("97", 0)):
            self.eq_(tools.is_year(mem[0]), mem[1])

class Test_generate_rand_str(UnitTestBase):
    """tools.generate_rand_str

    Note: This is a mediocre test because generate_rand_str produces a
    string that's of random length and random content.  It's possible
    for this test to pass even when the code is bad.
    """
    def _gen_checker(self, s, minlen, maxlen):
        assert len(s) >= minlen and len(s) <= maxlen
        for c in s:
            assert c in string.letters or c in string.digits

    def test_generates_a_random_string(self):
        for i in range(5):
            self._gen_checker(tools.generate_rand_str(), 5, 10)

    def test_generates_a_random_string_between_minlen_and_maxlen(self):
        for i in range(5):
             self._gen_checker(tools.generate_rand_str(4, 10), 4, 10)

        for i in range(5):
            self._gen_checker(tools.generate_rand_str(3, 12), 3, 12)

class Testescape_text(UnitTestBase):
    """tools.escape_text"""
    def test_none_to_none(self):
        self.eq_(tools.escape_text(None), None)

    def test_empty_string_to_empty_string(self):
        self.eq_(tools.escape_text(""), "")

    def test_single_quote_to_pos(self):
        self.eq_(tools.escape_text("a'b"), "a&#x27;b")

    def test_double_quote_to_quot(self):
        self.eq_(tools.escape_text("a\"b"), "a&quot;b")

    def test_greater_than(self):
        self.eq_(tools.escape_text("a>b"), "a&gt;b")

    def test_lesser_than(self):
        self.eq_(tools.escape_text("a<b"), "a&lt;b")

    def test_ampersand(self):
        self.eq_(tools.escape_text("a&b"), "a&amp;b")

    def test_complicated_case(self):
        self.eq_(tools.escape_text("a&>b"), "a&amp;&gt;b")

    def test_everything_else_unchanged(self):
        for mem in ((None, None),
                    ("", ""),
                    ("abc", "abc")):
            self.eq_(tools.escape_text(mem[0]), mem[1])

class Testurlencode_text(UnitTestBase):
    """tools.urlencode_text"""
    def test_none_to_none(self):
        self.eq_(tools.urlencode_text(None), None)

    def test_empty_string_to_empty_string(self):
        self.eq_(tools.urlencode_text(""), "")

    def test_equals_to_3D(self):
        self.eq_(tools.urlencode_text("a=c"), "a%3Dc")

    def test_ampersand_to_26(self):
        self.eq_(tools.urlencode_text("a&c"), "a%26c")

    def test_space_to_20(self):
        self.eq_(tools.urlencode_text("a c"), "a%20c")

    def test_utf8(self):
        self.eq_(tools.urlencode_text("español"), "espa%C3%B1ol")

    def test_everything_else_unchanged(self):
        for mem in ((None, None),
                    ("", ""),
                    ("abc", "abc")):
            self.eq_(tools.urlencode_text(mem[0]), mem[1])


class Testimportname(UnitTestBase):
    """tools.importname"""
    def setUp(self):
        UnitTestBase.setUp(self)
        tools._config = {}

    def tearDown(self):
        UnitTestBase.tearDown(self)
        if "_config" in tools.__dict__:
            del tools.__dict__["_config"]

    def _c(self, mn, n):
        m = tools.importname(mn, n)
        # print repr(m)
        return m

    def test_goodimport(self):
        import string
        self.eq_(tools.importname("", "string"), string)

        import os.path
        self.eq_(tools.importname("os", "path"), os.path)

    def test_badimport(self):
        self.eq_(tools.importname("", "foo"), None)

class Testwhat_ext(UnitTestBase):
    """tools.what_ext"""
    def get_ext_dir(self):
        return os.path.join(self.get_temp_dir(), "ext")
        
    def setUp(self):
        """
        Creates the directory with some files in it.
        """
        UnitTestBase.setUp(self)
        self._files = ["a.txt", "b.html", "c.txtl", "español.txt"]
        os.mkdir(self.get_ext_dir())

        for mem in self._files:
            f = open(os.path.join(self.get_ext_dir(), mem), "w")
            f.write("lorem ipsum")
            f.close()

    def test_returns_extension_if_file_has_extension(self):
        d = self.get_ext_dir()
        self.eq_(tools.what_ext(["txt", "html"], os.path.join(d, "a")),
                 "txt")
        self.eq_(tools.what_ext(["txt", "html"], os.path.join(d, "b")),
                 "html")
        self.eq_(tools.what_ext(["txt", "html"], os.path.join(d, "español")),
                 "txt")

    def test_returns_None_if_extension_not_present(self):
        d = self.get_ext_dir()
        self.eq_(tools.what_ext([], os.path.join(d, "a")), None)
        self.eq_(tools.what_ext(["html"], os.path.join(d, "a")), None)

## class Testrun_callback:
##     """tools.run_callback

##     This tests run_callback functionality.
##     """
##     def test_run_callback(self):
##         def fun1(args):
##             eq_(args["x"], 0)
##             return {"x": 1}

##         def fun2(args):
##             eq_(args["x"], 1)
##             return {"x": 2}

##         def fun3(args):
##             eq_(args["x"], 2)
##             return {"x": 3}

##         args = {"x": 0}
##         ret = tools.run_callback([fun1, fun2, fun3], args,
##                                  mappingfunc=lambda x,y: y)
##         eq_(ret["x"], 3)

class Testconvert_configini_values(UnitTestBase):
    """tools.convert_configini_values

    This tests config.ini -> config conversions.
    """
    def test_empty(self):
        self.eq_(tools.convert_configini_values({}), {})

    def test_no_markup(self):
        self.eq_(tools.convert_configini_values({"a": "b"}), {"a": "b"})

    def test_integers(self):
        for mem in (({"a": "1"}, {"a": 1}),
                    ({"a": "1", "b": "2"}, {"a": 1, "b": 2}),
                    ({"a": "10"}, {"a": 10}),
                    ({"a": "100"}, {"a": 100}),
                    ({"a": " 100  "}, {"a": 100})):
            self.eq_(tools.convert_configini_values(mem[0]), mem[1])

    def test_strings(self):
        for mem in (({"a": "'b'"}, {"a": "b"}),
                    ({"a": "\"b\""}, {"a": "b"}),
                    ({"a": "   \"b\" "}, {"a": "b"}),
                    ({"a": "español"}, {"a": "español"}),
                    ({"a": "'español'"}, {"a": "español"})):
            self.eq_(tools.convert_configini_values(mem[0]), mem[1])

    def test_lists(self):
        for mem in (({"a": "[]"}, {"a": []}),
                    ({"a": "[1]"}, {"a": [1]}),
                    ({"a": "[1, 2]"}, {"a": [1, 2]}),
                    ({"a": "  [1 ,2 , 3]"}, {"a": [1, 2, 3]}),
                    ({"a": "['1' ,\"2\" , 3]"}, {"a": ["1", "2", 3]})):
            self.eq_(tools.convert_configini_values(mem[0]), mem[1])

    def test_syntax_exceptions(self):
        for mem in ({"a": "'b"},
                    {"a": "b'"},
                    {"a": "\"b"},
                    {"a": "b\""},
                    {"a": "[b"},
                    {"a": "b]"}):
            self.assertRaises(tools.ConfigSyntaxErrorException,
                              tools.convert_configini_values, mem)

    # FIXME - test tools.walk

    # FIXME - test filestat
