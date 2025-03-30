import sys
import pkg_resources

try:
    import llama_stack_client
    print(f"llama_stack_client is installed. Version: {llama_stack_client.__version__}")
    
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted([f"{i.key}=={i.version}" for i in installed_packages])
    
    print("\nInstalled packages containing 'llama':")
    for pkg in installed_packages_list:
        if "llama" in pkg.lower():
            print(f"  {pkg}")
    
    print("\nVerification successful!")
    sys.exit(0)
except ImportError as e:
    print(f"Error importing llama_stack_client: {e}")
    print("\nThe package is not properly installed or importable.")
    sys.exit(1)
