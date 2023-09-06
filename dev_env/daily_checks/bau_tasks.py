def run_bsp_bau_tasks():
    """ 
    1) Monitor health endpoints: call each microservices /health endpoint 
    and append to actions list if any are marked as DOWN. 

    Example of data to work with:

    2) Warn if expiration dates for certificates are upcoming (within a month), 
    or show an error if they have been exceeded. Add an action in both cases to 
    the actions list to print out at the end of the script

    Example to work with: input file json, where dates need to be changed manually for now

    3) Check stale envelopes in blob router - this should always be empty. In the case it isn't, 
    add an action to the list

    4) Stale envelopes in processor - should be empty, if not then do a PUT request to make 
    the envelope reprocess itself as an exception record so that a caseworker can investigate further
    
    """
    print('to do')