from run_cumulus_task import run_cumulus_task

from dmrpp_generator.main import main


def handler(event, context):
    # print(f'CMA Event: {event}')
    if 'cma' in event:
        print(f'Running cumulus task...')
        ret = run_cumulus_task(main, event, context)
    else:
        print(f'Calling main()...')
        ret = main(event, context)

    return ret
