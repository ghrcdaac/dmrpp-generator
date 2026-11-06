"""Lambda handler for DMRPP generator."""

from run_cumulus_task import run_cumulus_task

from .main import main


def handler(event, context):
    """Run DMRPP generator as a lambda.
    Runs as a Cumulus task if CMA input detected.
    """
    # print(f"CMA Event: {event}")
    if "cma" in event:
        print("Running cumulus task...")
        ret = run_cumulus_task(main, event, context)
    else:
        print("Calling main()...")
        ret = main(event, context)

    return ret
