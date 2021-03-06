import boto3

class Cognito(object):
    def __init__(self, region, profile):
        self.region = region
        self.profile = profile
        self.client = boto3.client('cognito-idp')
        self._user_pools = self.list_user_pools()

    def list_user_pools(self):
        call = self.client.list_user_pools(MaxResults=50)
        result = call['UserPools']
        while "NextToken" in call and call['NextToken']:
            token = call["NextToken"]
            call = self.client.list_user_pools(NextToken=token)
            result += call['UserPools']
        return result

    def get_user_pool_id(self, user_pool_name):
        for user_pool in self._user_pools:
            if user_pool['Name'] == user_pool_name:
                user_pool_id = user_pool['Id']
                return user_pool_id

    def list_users(self, user_pool_name):
        call = self.client.list_users(
                UserPoolId = self.get_user_pool_id(user_pool_name),
                Limit = 50
            )
        users = call['Users']
        while 'PaginationToken' in call and call['PaginationToken']:
            token = call['PaginationToken']
            call = self.client.list_users(
                        UserPoolId = self.get_user_pool_id(user_pool_name),
                        PaginationToken = token,
                        Limit = 50
                    )
            users += call['Users']
        return users

    def list_user_pool_clients(self, user_pool_name):
        call = self.client.list_user_pool_clients(
            UserPoolId = self.get_user_pool_id(user_pool_name),
            MaxResults = 50,
        )
        clients = call['UserPoolClients']
        while "NextToken" in call and call['NextToken']:
            call = self.client.list_user_pool_clients(
                        UserPoolId = user_pool_id,
                        NextToken = call["NextToken"],
                        MaxResults=50,
                    )
            clients += call['UserPoolClients']
        return clients

    def describe_user_pool(self, user_pool):
        detail_to_add = ["Domain", "UserPoolTags", "EstimatedNumberOfUsers"]
        call = self.client.describe_user_pool(
                    UserPoolId = user_pool['Id']
                )['UserPool']
        for key in detail_to_add:
            user_pool[key] = call[key]

        return user_pool

    @property
    def user_pools(self):
        return self._user_pools
