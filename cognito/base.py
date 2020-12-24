import boto3

class Cognito(object):
    def __init__(self, region, profile):
        self.region = region
        self.profile = profile
        self.client = boto3.client('cognito-idp')
        self._user_pools = self.list_user_pools()

    def list_user_pools(self):
        result = []
        call = self.client.list_user_pools(MaxResults=50)
        result = call['UserPools']
        while "NextToken" in call and call['NextToken']:
            token = call["NextToken"]
            call = self.client.list_user_pools(NextToken=token)
            result += call['UserPools']
        return result

    def list_users(self, user_pool_name):
        for user_pool in self._user_pools:
            if user_pool['Name'] == user_pool_name:
                user_pool_id = user_pool['Id']

        users = []
        call = self.client.list_users(
                UserPoolId = user_pool_id,
                Limit = 50
            )
        users = call['Users']
        while 'PaginationToken' in call and call['PaginationToken']:
            token = call['PaginationToken']
            call = self.client.list_users(
                        UserPoolId = user_pool_id,
                        PaginationToken = token,
                        Limit = 50
                    )
            users += call['Users']
            
        return users

    @property
    def user_pools(self):
        return self._user_pools