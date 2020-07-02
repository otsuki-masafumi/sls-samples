import boto3

def handler(event, context):
    sm_arn = event['sm_arn']
    execution_name = event['execution_name']
    
    # 指定されたState MachineのExecution一覧（直近20件）を取得する
    sfn_client = boto3.client('stepfunctions')
    execution_list = sfn_client.list_executions(stateMachineArn=sm_arn, maxResults=20)

    # execution_nameを部分文字列として含むexecutionのみを取り出す
    target_execution = [x for x in execution_list['executions'] if execution_name in x['name']]

    # execution_nameが含まれるexecutionのステータスを取り出す
    status = [x['status'] for x in target_execution]
    
    # executionの状態によってチェック結果を反映する
    if len(status) == 0:
        # まだ実行してないから実行する
        check_status = 0
        execution_status = "NOTEXIST"
    
    elif 'SUCCEEDED' in status:
        # もう正常終了しているからスキップする
        check_status = 1
        execution_status = 'SUCCEEDED'
    else:
        # それ以外の状態では実行できないので失敗させる
        check_status = 2
        execution_status = 'OTHER'
        
    return {'check_result': check_status , "execution_status": execution_status}