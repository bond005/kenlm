from setuptools import setup, Extension
import glob
import platform
import os

#Does gcc compile with this header and library?
def compile_test(header, library):
    dummy_path = os.path.join(os.path.dirname(__file__), "dummy")
    command = "bash -c \"g++ -include " + header + " -l" + library + " -x c++ - <<<'int main() {}' -o " + dummy_path + " >/dev/null 2>/dev/null && rm " + dummy_path + " 2>/dev/null\""
    return os.system(command) == 0


FILES = glob.glob(os.path.join('util', '*.cc')) + glob.glob(os.path.join('lm', '*.cc')) + glob.glob(os.path.join('util', 'double-conversion/*.cc'))
FILES = [fn for fn in FILES if not (fn.endswith('main.cc') or fn.endswith('test.cc'))]

if platform.system() == 'Linux':
    LIBS = ['stdc++', 'rt']
elif platform.system() == 'Darwin':
    LIBS = ['stdc++']
else:
    LIBS = []

#We don't need -std=c++11 but python seems to be compiled with it now.  https://github.com/kpu/kenlm/issues/86
if platform.system() == 'Windows':
    ARGS = ['/O2', '/DNDEBUG', '/DKENLM_MAX_ORDER=6', '/D_CRT_NONSTDC_NO_WARNINGS']
else:
    ARGS = ['-O3', '-DNDEBUG', '-DKENLM_MAX_ORDER=6', '-std=c++11']

if platform.system() != 'Windows':
    if compile_test('zlib.h', 'z'):
        ARGS.append('-DHAVE_ZLIB')
        LIBS.append('z')

    if compile_test('bzlib.h', 'bz2'):
        ARGS.append('-DHAVE_BZLIB')
        LIBS.append('bz2')

    if compile_test('lzma.h', 'lzma'):
        ARGS.append('-DHAVE_XZLIB')
        LIBS.append('lzma')

ext_modules = [
    Extension(name='kenlm',
        sources=FILES + [os.path.join('python', 'kenlm.cpp')],
        language='C++', 
        include_dirs=['.'],
        libraries=LIBS, 
        extra_compile_args=ARGS)
]

setup(
    name='kenlm',
    ext_modules=ext_modules,
    include_package_data=True,
)
