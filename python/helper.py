import shutil
import sys
import os.path
import os
import subprocess

def _check_available(executable_name):
    """Return True if the executable_name is found in the search path."""
    return (shutil.which(executable_name) is not None) or os.path.isfile(executable_name)

def package_available(package_name):
    """Return True if package_name is installed."""
    return _check_available("glpsol") if package_name == "glpk" else _check_available(package_name)

def package_found(package_name):
    """Print message confirming that package was found, then return True or False."""
    is_available = package_available(package_name)
    if is_available:
        print(f"{package_name} was previously installed")
    return is_available

def package_confirm(package_name):
    """Confirm package is available after installation."""
    if package_available(package_name):
        print("installation successful")
        return True
    else:
        print("installation failed")
        return False

def on_colab(): 
    """Return True if running on Google Colab."""
    return "google.colab" in sys.modules

def install_pyomo():
    """Install pyomo from idaes_pse to include enhanced LA solvers."""
    if package_found("pyomo"):
        return True
    print("Installing pyomo from idaes_pse via pip ... ", end="")
    os.system("pip install -q idaes_pse")
    return package_confirm("pyomo")

def install_idaes():
    if package_found("idaes"):
        return
    print("Installing idaes from idaes_pse via pip ... ", end="")
    os.system("pip install -q idaes_pse")
    return package_confirm("idaes")

def install_ipopt():
    if package_found("ipopt"):
        return True

    # try idaes version of ipopt with HSL solvers
    if on_colab():
        # Install idaes solvers
        print("Installing ipopt and k_aug on Google Colab via idaes get-extensions ... ", end="")
        os.system("idaes get-extensions")

        # Add symbolic link for idaes solvers
        os.system("ln -s /root/.idaes/bin/ipopt ipopt")
        os.system("ln -s /root/.idaes/bin/k_aug k_aug")
    
    # check again
    if package_confirm("ipopt"):
        return True

    # try coin-OR version of ipopt with mumps solvers
    if on_colab():
        print("Installing ipopt on Google Colab via zip file ... ", end="")
        os.system('wget -N -q "https://ampl.com/dl/open/ipopt/ipopt-linux64.zip"')
        os.system('!unzip -o -q ipopt-linux64')
    else:
        print("Installing Ipopt via conda ... ", end="")
        os.system('conda install -c conda-forge ipopt')
    return package_confirm("ipopt")

def install_glpk():
    if package_found("glpk"):
        return True
    if on_colab():
        print("Installing glpk on Google Colab via apt-get ... ", end="")
        os.system('apt-get install -y -qq glpk-utils')
    else:
        print("Installing glpk via conda ... ", end="")
        os.system('conda install -c conda-forge glpk')
    return package_confirm("glpk")

def install_cbc():
    if package_found("cbc"):
        return True
    if on_colab():
        print("Installing cbc on Google Colab via zip file ... ", end="")
        os.system('wget -N -q "https://ampl.com/dl/open/cbc/cbc-linux64.zip"')
        os.system('unzip -o -q cbc-linux64')
    else:
        print("Installing cbc via apt-get ... ", end="")
        os.system('apt-get install -y -qq coinor-cbc')
    return package_confirm("cbc")
        
def install_bonmin():
    if package_found("bonmin"):
        return True
    if on_colab():
        print("Installing bonmin on Google Colab via zip file ... ", end="")
        os.system('wget -N -q "https://ampl.com/dl/open/bonmin/bonmin-linux64.zip"')
        os.system('unzip -o -q bonmin-linux64')
    else:
        print("No procedure implemented to install bonmin ... ", end="")
    return package_confirm("bonmin")

def install_couenne():
    if package_found("couenne"):
        return
    if on_colab():
        print("Installing couenne on Google Colab via via zip file ... ", end="")
        os.system('wget -N -q "https://ampl.com/dl/open/couenne/couenne-linux64.zip"')
        os.system('unzip -o -q couenne-linux64')
    else:
        print("No procedure implemented to install couenne ... ", end="")
    return package_confirm("couenne")

def install_gecode():
    if package_found("gecode"):
        return
    if on_colab():
        print("Installing gecode on Google Colab via via zip file ... ", end="")
        os.system('wget -N -q "https://ampl.com/dl/open/gecode/gecode-linux64.zip"')
        os.system('unzip -o -q gecode-linux64')
    else:
        print("No procedure implemented to install gecode ... ", end="")
    return package_confirm("gecode")

def install_scip():
    if package_found("scip"):
        return

    if on_colab():
        print("Installing scip on Google Colab via conda ... ", end="")
        try:
            import condacolab
        except:
            os.system("pip install -q condacolab")
            import condacolab
            condacolab.install()
        os.system("conda install -y pyscipopt")

    return package_confirm("scip")

def install_gurobi():
    try:
        import gurobipy
    except ImportError:
        pass
    else:
        print("gurobi was previously installed")
        return

    if on_colab():
        print("Installing gurobi on Google Colab via pip ... ", end="")
        os.system("pip install gurobipy")
    else:
        print("Consult gurobi.com for installation procedures ... ", end="")

    try:
        import gurobipy
        print("installation successful")
        return True
    except ImportError:
        print("installation failed")
        return False

def install_cplex():
    try:
        import cplex
    except ImportError:
        pass
    else:
        print("cplex was previously installed")
        return

    if on_colab():
        print("Installing cplex on Google Colab via pip ... ", end="")
        os.system("pip install cplex")
    else:
        print("Consult ibm.com for installation procedures ... ", end="")

    try:
        import cplex
        print("installation successful")
        return True
    except ImportError:
        print("installation failed")
        return False

def install_mosek():
    try:
        import mosek.fusion
    except ImportError:
        pass
    else:
        print("mosek was previously installed")
        return

    if on_colab():
        print("Installing mosek on Google Colab via pip ... ", end="")
        os.system("pip install mosek")
    else:
        print("Consult docs.mosek.com for installation procedures ... ", end="")

    try:
        import mosek.fusion
        print("installation successful")
        return True
    except ImportError:
        print("installation failed.")
        return False

def install_xpress():
    try:
        import xpress
    except ImportError:
        pass
    else:
        print("Xpress was previously installed")
        return
    
    if on_colab():
        print("Installing xpress on Google Colab via pip ... ", end="")
        os.system("pip install xpress")
    else:
        print("Installing xpress via conda ... ", end="")
        os.system("conda install -c fico-xpress xpress")

    try:
        import xpress
        print("installation successful")
        return True
    except ImportError:
        print("installation failed")
        return False
 
