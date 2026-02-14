import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from datetime import datetime

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 데이터 파일
DATA_FILE = 'chicken_penalties.json'

# 데이터 로드/저장 함수
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'penalties': [], 'next_id': 1}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@bot.event
async def on_ready():
    print(f'{bot.user} 봇이 준비되었습니다!')
    try:
        synced = await bot.tree.sync()
        print(f'{len(synced)}개의 명령어가 동기화되었습니다.')
    except Exception as e:
        print(f'명령어 동기화 실패: {e}')

# 벌칙 추가
@bot.tree.command(name="벌칙추가", description="꼴등 팀 치킨 벌칙 등록")
@app_commands.describe(
    팀원들="팀원 이름 (쉼표로 구분)",
    날짜="날짜 (선택사항, 기본값: 오늘)"
)
async def add_penalty(interaction: discord.Interaction, 팀원들: str, 날짜: str = None):
    data = load_data()
    
    # 날짜 처리
    if 날짜 is None:
        날짜 = datetime.now().strftime('%Y-%m-%d')
    
    # 팀원 리스트 생성
    losers = [name.strip() for name in 팀원들.split(',')]
    
    # 벌칙 추가
    penalty = {
        'id': data['next_id'],
        'date': 날짜,
        'losers': losers,
        'verified': False,
        'created_at': datetime.now().isoformat(),
        'created_by': str(interaction.user)
    }
    
    data['penalties'].append(penalty)
    data['next_id'] += 1
    save_data(data)
    
    # 임베드 생성
    embed = discord.Embed(
        title="🍗 치킨 벌칙 등록 완료!",
        description=f"**날짜:** {날짜}\n**꼴등 팀:** {', '.join(losers)}",
        color=discord.Color.orange()
    )
    embed.add_field(name="벌칙 ID", value=f"#{penalty['id']}", inline=True)
    embed.add_field(name="상태", value="❌ 미인증", inline=True)
    embed.set_footer(text=f"등록자: {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed)

# 인증
@bot.tree.command(name="인증", description="치킨 먹은 사진 인증")
@app_commands.describe(벌칙id="인증할 벌칙 ID")
async def verify(interaction: discord.Interaction, 벌칙id: int):
    data = load_data()
    
    # 벌칙 찾기
    penalty = None
    for p in data['penalties']:
        if p['id'] == 벌칙id:
            penalty = p
            break
    
    if penalty is None:
        await interaction.response.send_message(f"❌ 벌칙 ID #{벌칙id}를 찾을 수 없습니다.", ephemeral=True)
        return
    
    if penalty['verified']:
        await interaction.response.send_message(f"✅ 이미 인증된 벌칙입니다.", ephemeral=True)
        return
    
    # 인증 처리
    penalty['verified'] = True
    penalty['verified_at'] = datetime.now().isoformat()
    penalty['verified_by'] = str(interaction.user)
    save_data(data)
    
    embed = discord.Embed(
        title="✅ 치킨 인증 완료!",
        description=f"**벌칙 ID:** #{벌칙id}\n**날짜:** {penalty['date']}\n**팀원:** {', '.join(penalty['losers'])}",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"인증자: {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed)

# 인증 취소
@bot.tree.command(name="인증취소", description="치킨 인증 취소")
@app_commands.describe(벌칙id="취소할 벌칙 ID")
async def unverify(interaction: discord.Interaction, 벌칙id: int):
    data = load_data()
    
    penalty = None
    for p in data['penalties']:
        if p['id'] == 벌칙id:
            penalty = p
            break
    
    if penalty is None:
        await interaction.response.send_message(f"❌ 벌칙 ID #{벌칙id}를 찾을 수 없습니다.", ephemeral=True)
        return
    
    if not penalty['verified']:
        await interaction.response.send_message(f"❌ 미인증 상태입니다.", ephemeral=True)
        return
    
    penalty['verified'] = False
    penalty.pop('verified_at', None)
    penalty.pop('verified_by', None)
    save_data(data)
    
    await interaction.response.send_message(f"✅ 벌칙 ID #{벌칙id}의 인증이 취소되었습니다.")

# 목록 조회
@bot.tree.command(name="벌칙목록", description="치킨 벌칙 목록 보기")
@app_commands.describe(상태="전체/미인증/인증완료")
async def list_penalties(interaction: discord.Interaction, 상태: str = "전체"):
    data = load_data()
    penalties = data['penalties']
    
    # 필터링
    if 상태 == "미인증":
        penalties = [p for p in penalties if not p['verified']]
    elif 상태 == "인증완료":
        penalties = [p for p in penalties if p['verified']]
    
    if not penalties:
        await interaction.response.send_message(f"📋 {상태} 벌칙이 없습니다.")
        return
    
    # 최신순 정렬
    penalties = sorted(penalties, key=lambda x: x['created_at'], reverse=True)
    
    # 임베드 생성
    embed = discord.Embed(
        title=f"🍗 치킨 벌칙 목록 ({상태})",
        description=f"총 {len(penalties)}건",
        color=discord.Color.orange() if 상태 == "미인증" else discord.Color.green()
    )
    
    # 최대 10개만 표시
    for penalty in penalties[:10]:
        status = "✅ 인증완료" if penalty['verified'] else "❌ 미인증"
        value = f"**날짜:** {penalty['date']}\n**팀원:** {', '.join(penalty['losers'])}\n**상태:** {status}"
        embed.add_field(
            name=f"벌칙 ID #{penalty['id']}",
            value=value,
            inline=False
        )
    
    if len(penalties) > 10:
        embed.set_footer(text=f"+ {len(penalties) - 10}건 더 있음")
    
    await interaction.response.send_message(embed=embed)

# 통계
@bot.tree.command(name="치킨통계", description="개인별 치킨 벌칙 통계")
async def stats(interaction: discord.Interaction):
    data = load_data()
    penalties = data['penalties']
    
    if not penalties:
        await interaction.response.send_message("📊 아직 통계가 없습니다.")
        return
    
    # 개인별 집계
    stats = {}
    for penalty in penalties:
        for loser in penalty['losers']:
            if loser not in stats:
                stats[loser] = {'total': 0, 'verified': 0}
            stats[loser]['total'] += 1
            if penalty['verified']:
                stats[loser]['verified'] += 1
    
    # 정렬 (총 벌칙 많은 순)
    sorted_stats = sorted(stats.items(), key=lambda x: x[1]['total'], reverse=True)
    
    # 임베드 생성
    embed = discord.Embed(
        title="📊 치킨 벌칙 통계",
        description=f"총 {len(penalties)}건의 벌칙",
        color=discord.Color.gold()
    )
    
    for name, data in sorted_stats:
        percentage = (data['verified'] / data['total'] * 100) if data['total'] > 0 else 0
        value = f"총 {data['total']}회 | 인증 {data['verified']}회 ({percentage:.0f}%)"
        
        # 진행률 바 생성
        bar_length = 10
        filled = int(percentage / 10)
        bar = '🟩' * filled + '⬜' * (bar_length - filled)
        
        embed.add_field(
            name=f"{name} 🍗",
            value=f"{value}\n{bar}",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

# 삭제
@bot.tree.command(name="벌칙삭제", description="벌칙 기록 삭제 (관리자만)")
@app_commands.describe(벌칙id="삭제할 벌칙 ID")
async def delete_penalty(interaction: discord.Interaction, 벌칙id: int):
    # 관리자 권한 체크
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ 관리자만 삭제할 수 있습니다.", ephemeral=True)
        return
    
    data = load_data()
    
    # 벌칙 찾기
    penalty_index = None
    for i, p in enumerate(data['penalties']):
        if p['id'] == 벌칙id:
            penalty_index = i
            break
    
    if penalty_index is None:
        await interaction.response.send_message(f"❌ 벌칙 ID #{벌칙id}를 찾을 수 없습니다.", ephemeral=True)
        return
    
    # 삭제
    deleted = data['penalties'].pop(penalty_index)
    save_data(data)
    
    await interaction.response.send_message(
        f"✅ 벌칙 ID #{벌칙id} (날짜: {deleted['date']}, 팀원: {', '.join(deleted['losers'])})가 삭제되었습니다."
    )

# 도움말
@bot.tree.command(name="치킨도움말", description="봇 사용법 안내")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🍗 치킨 벌칙 봇 사용법",
        description="배그 꼴등 팀은 치킨을 먹어야 합니다!",
        color=discord.Color.blue()
    )
    
    commands_info = [
        ("**/벌칙추가**", "`/벌칙추가 팀원들:철수,영희,민수 [날짜:2024-01-15]`\n꼴등 팀 벌칙 등록"),
        ("**/인증**", "`/인증 벌칙id:1`\n치킨 먹고 인증하기"),
        ("**/인증취소**", "`/인증취소 벌칙id:1`\n인증 취소하기"),
        ("**/벌칙목록**", "`/벌칙목록 [상태:미인증]`\n벌칙 목록 보기 (전체/미인증/인증완료)"),
        ("**/치킨통계**", "`/치킨통계`\n개인별 통계 확인"),
        ("**/벌칙삭제**", "`/벌칙삭제 벌칙id:1`\n벌칙 삭제 (관리자만)")
    ]
    
    for cmd, desc in commands_info:
        embed.add_field(name=cmd, value=desc, inline=False)
    
    embed.set_footer(text="문의: 클랜 관리자에게 연락하세요")
    
    await interaction.response.send_message(embed=embed)

# 봇 실행
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    # .env 파일에서 환경 변수 로드
    load_dotenv()
    
    # 환경 변수에서 토큰 가져오기
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    if not TOKEN:
        print("❌ 에러: DISCORD_TOKEN 환경 변수가 설정되지 않았습니다.")
        print("Railway에서 Variables 탭에서 DISCORD_TOKEN을 설정해주세요.")
        print("또는 .env 파일에 DISCORD_TOKEN=여기에_토큰 형태로 추가해주세요.")
        exit(1)
    
    print("🤖 봇을 시작합니다...")
    print(f"🔗 봇 사용자: {bot.user if bot.user else '로그인 대기 중...'}")
    
    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        print("❌ 로그인 실패: 봇 토큰이 올바르지 않습니다.")
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
