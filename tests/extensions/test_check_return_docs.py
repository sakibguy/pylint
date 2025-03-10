# Copyright (c) 2016-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016, 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2016 Glenn Matthews <glenn@e-dad.net>
# Copyright (c) 2016 Moises Lopez <moylop260@vauxoo.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2019 Zeb Nicholls <zebedee.nicholls@climate-energy-college.org>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Unit tests for the return documentation checking in the
`DocstringChecker` in :mod:`pylint.extensions.check_docs`
"""

# pylint: disable=too-many-public-methods

import astroid

from pylint.extensions.docparams import DocstringParameterChecker
from pylint.testutils import CheckerTestCase, Message, set_config


class TestDocstringCheckerReturn(CheckerTestCase):
    """Tests for pylint_plugin.RaiseDocChecker"""

    CHECKER_CLASS = DocstringParameterChecker

    def test_ignores_no_docstring(self) -> None:
        return_node = astroid.extract_node(
            """
        def my_func(self):
            return False #@
        """
        )
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    @set_config(accept_no_return_doc=False)
    def test_warns_no_docstring(self) -> None:
        node = astroid.extract_node(
            """
        def my_func(self):
            return False
        """
        )
        return_node = node.body[0]
        with self.assertAddsMessages(
            Message(msg_id="missing-return-doc", node=node),
            Message(msg_id="missing-return-type-doc", node=node),
        ):
            self.checker.visit_return(return_node)

    def test_ignores_unknown_style(self) -> None:
        return_node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring."""
            return False #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_warn_partial_sphinx_returns(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            :returns: Always False
            """
            return False
        '''
        )
        return_node = node.body[0]
        with self.assertAddsMessages(
            Message(msg_id="missing-return-type-doc", node=node)
        ):
            self.checker.visit_return(return_node)

    def test_sphinx_missing_return_type_with_annotations(self) -> None:
        node = astroid.extract_node(
            '''
           def my_func(self) -> bool:
               """This is a docstring.

               :returns: Always False
               """
               return False
           '''
        )
        return_node = node.body[0]
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_warn_partial_sphinx_returns_type(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            :rtype: bool
            """
            return False
        '''
        )
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id="missing-return-doc", node=node)):
            self.checker.visit_return(return_node)

    def test_warn_missing_sphinx_returns(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self, doc_type):
            """This is a docstring.

            :param doc_type: Sphinx
            :type doc_type: str
            """
            return False
        '''
        )
        return_node = node.body[0]
        with self.assertAddsMessages(
            Message(msg_id="missing-return-doc", node=node),
            Message(msg_id="missing-return-type-doc", node=node),
        ):
            self.checker.visit_return(return_node)

    def test_warn_partial_google_returns(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns:
                Always False
            """
            return False
        '''
        )
        return_node = node.body[0]
        with self.assertAddsMessages(
            Message(msg_id="missing-return-type-doc", node=node)
        ):
            self.checker.visit_return(return_node)

    def test_warn_partial_google_returns_type(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns:
                bool:
            """
            return False
        '''
        )
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id="missing-return-doc", node=node)):
            self.checker.visit_return(return_node)

    def test_warn_missing_google_returns(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self, doc_type):
            """This is a docstring.

            Parameters:
                doc_type (str): Google
            """
            return False
        '''
        )
        return_node = node.body[0]
        with self.assertAddsMessages(
            Message(msg_id="missing-return-doc", node=node),
            Message(msg_id="missing-return-type-doc", node=node),
        ):
            self.checker.visit_return(return_node)

    def test_warn_partial_numpy_returns_type(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self, doc_type):
            """This is a docstring.

            Arguments
            ---------
            doc_type : str
                Numpy

            Returns
            -------
            bool
            """
            return False
        '''
        )
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id="missing-return-doc", node=node)):
            self.checker.visit_return(return_node)

    def test_warn_missing_numpy_returns(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self, doc_type):
            """This is a docstring.

            Arguments
            ---------
            doc_type : str
                Numpy
            """
            return False
        '''
        )
        return_node = node.body[0]
        with self.assertAddsMessages(
            Message(msg_id="missing-return-doc", node=node),
            Message(msg_id="missing-return-type-doc", node=node),
        ):
            self.checker.visit_return(return_node)

    def test_find_sphinx_returns(self) -> None:
        return_node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            :return: Always False
            :rtype: bool
            """
            return False #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_find_google_returns(self) -> None:
        return_node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns:
                bool: Always False
            """
            return False #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_find_numpy_returns(self) -> None:
        return_node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns
            -------
            bool
                Always False
            """
            return False #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_find_numpy_returns_with_of(self) -> None:
        return_node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns
            -------
            :obj:`list` of :obj:`str`
                List of strings
            """
            return ["hi", "bye"] #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_ignores_sphinx_return_none(self) -> None:
        return_node = astroid.extract_node(
            '''
        def my_func(self, doc_type):
            """This is a docstring.

            :param doc_type: Sphinx
            :type doc_type: str
            """
            return #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_ignores_google_return_none(self) -> None:
        return_node = astroid.extract_node(
            '''
        def my_func(self, doc_type):
            """This is a docstring.

            Args:
                doc_type (str): Google
            """
            return #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_ignores_numpy_return_none(self) -> None:
        return_node = astroid.extract_node(
            '''
        def my_func(self, doc_type):
            """This is a docstring.

            Arguments
            ---------
            doc_type : str
                Numpy
            """
            return #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_finds_sphinx_return_custom_class(self) -> None:
        return_node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            :returns: An object
            :rtype: :class:`mymodule.Class`
            """
            return mymodule.Class() #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_finds_google_return_custom_class(self) -> None:
        return_node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns:
                mymodule.Class: An object
            """
            return mymodule.Class() #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_finds_numpy_return_custom_class(self) -> None:
        return_node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns
            -------
                mymodule.Class
                    An object
            """
            return mymodule.Class() #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_finds_sphinx_return_list_of_custom_class(self) -> None:
        return_node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            :returns: An object
            :rtype: list(:class:`mymodule.Class`)
            """
            return [mymodule.Class()] #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_finds_google_return_list_of_custom_class(self) -> None:
        return_node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns:
                list(:class:`mymodule.Class`): An object
            """
            return [mymodule.Class()] #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_finds_numpy_return_list_of_custom_class(self) -> None:
        return_node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns
            -------
                list(:class:`mymodule.Class`)
                    An object
            """
            return [mymodule.Class()] #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_warns_sphinx_return_list_of_custom_class_without_description(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            :rtype: list(:class:`mymodule.Class`)
            """
            return [mymodule.Class()]
        '''
        )
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id="missing-return-doc", node=node)):
            self.checker.visit_return(return_node)

    def test_warns_google_return_list_of_custom_class_without_description(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns:
                list(:class:`mymodule.Class`):
            """
            return [mymodule.Class()]
        '''
        )
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id="missing-return-doc", node=node)):
            self.checker.visit_return(return_node)

    def test_warns_numpy_return_list_of_custom_class_without_description(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns
            -------
                list(:class:`mymodule.Class`)
            """
            return [mymodule.Class()]
        '''
        )
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id="missing-return-doc", node=node)):
            self.checker.visit_return(return_node)

    def test_warns_sphinx_redundant_return_doc(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            :returns: One
            """
            return None
        '''
        )
        with self.assertAddsMessages(
            Message(msg_id="redundant-returns-doc", node=node)
        ):
            self.checker.visit_functiondef(node)

    def test_warns_sphinx_redundant_rtype_doc(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            :rtype: int
            """
            return None
        '''
        )
        with self.assertAddsMessages(
            Message(msg_id="redundant-returns-doc", node=node)
        ):
            self.checker.visit_functiondef(node)

    def test_warns_google_redundant_return_doc(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns:
                One
            """
            return None
        '''
        )
        with self.assertAddsMessages(
            Message(msg_id="redundant-returns-doc", node=node)
        ):
            self.checker.visit_functiondef(node)

    def test_warns_google_redundant_rtype_doc(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns:
                int:
            """
            return None
        '''
        )
        with self.assertAddsMessages(
            Message(msg_id="redundant-returns-doc", node=node)
        ):
            self.checker.visit_functiondef(node)

    def test_warns_numpy_redundant_return_doc(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns
            -------
                int
                    One
            """
            return None
        '''
        )
        with self.assertAddsMessages(
            Message(msg_id="redundant-returns-doc", node=node)
        ):
            self.checker.visit_functiondef(node)

    def test_warns_numpy_redundant_rtype_doc(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns
            -------
                int
            """
            return None
        '''
        )
        with self.assertAddsMessages(
            Message(msg_id="redundant-returns-doc", node=node)
        ):
            self.checker.visit_functiondef(node)

    def test_ignores_sphinx_redundant_return_doc_multiple_returns(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            :returns: One
            :rtype: int

            :returns: None sometimes
            :rtype: None
            """
            if a_func():
                return None
            return 1
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_ignores_google_redundant_return_doc_multiple_returns(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns:
                int or None: One, or sometimes None.
            """
            if a_func():
                return None
            return 1
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_ignores_numpy_redundant_return_doc_multiple_returns(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns
            -------
                int
                    One
                None
                    Sometimes
            """
            if a_func():
                return None
            return 1
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_ignore_sphinx_redundant_return_doc_yield(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func_with_yield(self):
            """This is a docstring.

            :returns: One
            :rtype: generator
            """
            for value in range(3):
                yield value
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_warns_google_redundant_return_doc_yield(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns:
                int: One
            """
            yield 1
        '''
        )
        with self.assertAddsMessages(
            Message(msg_id="redundant-returns-doc", node=node)
        ):
            self.checker.visit_functiondef(node)

    def test_warns_numpy_redundant_return_doc_yield(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns
            -------
                int
                    One
            """
            yield 1
        '''
        )
        with self.assertAddsMessages(
            Message(msg_id="redundant-returns-doc", node=node)
        ):
            self.checker.visit_functiondef(node)
