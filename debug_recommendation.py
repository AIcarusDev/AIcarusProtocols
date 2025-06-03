import sys
sys.path.append('src')
from aicarus_protocols.common import event_registry

# 先运行平台架构注册
from aicarus_protocols.dynamic_examples import demo_platform_specific_schemas
demo_platform_specific_schemas()

print('\n=== 调试推荐系统 ===')
print('QQ平台事件类型:')
qq_types = event_registry.get_platform_types('qq')
for t in qq_types:
    print(f'  {t}')

print(f'\nQQ平台总计: {len(qq_types)} 个事件类型')

print('\n测试推荐 send_message:')
suggestions = event_registry.suggest_event_type('qq', 'send_message', 'group')
print(f'推荐结果: {suggestions}')

print('\n相关性评分测试:')
test_types = ['action.qq.send_group_msg', 'message.qq.group', 'action.qq.send_private_msg']
for event_type in test_types:
    if event_type in qq_types:
        score = event_registry._calculate_type_relevance(event_type, 'send_message', 'group')
        print(f'{event_type}: {score}')
    else:
        print(f'{event_type}: 不在注册列表中')

print('\n测试更简单的关键词匹配:')
for event_type in qq_types:
    if 'send' in event_type:
        score = event_registry._calculate_type_relevance(event_type, 'send', '')
        print(f'{event_type}: {score}')
