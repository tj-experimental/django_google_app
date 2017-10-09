from __future__ import unicode_literals

from pipeline.compilers.es6 import ES6Compiler


class ES6ModifiedCompiler(ES6Compiler):

    def match_file(self, path):
        return path.endswith('.es6')

    def is_outdated(self, infile, outfile):
        return True

    def compile_file(self, infile, outfile, outdated=False, force=False):
        import pdb
        pdb.set_trace()
        return super(ES6ModifiedCompiler, self).compile_file(
            infile=infile, outfile=outfile,
            outdated=outdated, force=force)
