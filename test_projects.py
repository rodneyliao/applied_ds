import pytest
import os
import papermill as pm
import glob

@pytest.mark.parametrize('folder', [x[0] for x in os.walk(os.getcwd())\
                                    if (len(x[0].split('/'))\
                                        == len(os.getcwd().split('/'))+1\
                                        and x[0].split('/')[-1][0] not in ['_', '.'])])
def test(folder):
    if folder == 'lecture_notes':
        pass
    os.chdir(folder)
    print(os.getcwd())
    for notebook in glob.glob('*.ipynb'):
        try: 
            pm.execute_notebook(
            notebook,
           'result.ipynb')
        finally:
            assert(os.path.isfile('%s/result.ipynb' % folder)), "Notebook did not run"
            os.remove('%s/result.ipynb' % folder)
    os.chdir(os.path.dirname(os.getcwd()))
    pass