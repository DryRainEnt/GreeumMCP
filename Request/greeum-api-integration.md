# Greeum API 통합 가이드

**최종 업데이트**: 2025-06-12 (v0.6.1 배포 완료)

## 작업 요약

MemoryEngine(Greeum) 프로젝트의 API 시스템을 분석하고 문서화했습니다. 이 문서는 외부 서비스에서 Greeum API를 통합하는 방법을 설명합니다.

## 프로젝트 개요

Greeum은 대화형 AI를 위한 블록체인 기반 장기 기억 관리 시스템입니다. 주요 특징:

- **블록체인 메모리**: 변경 불가능한 블록 구조로 메모리 무결성 보장
- **하이브리드 검색**: 의미적 임베딩과 키워드 기반 검색 결합
- **메모리 진화**: 수정 이력 추적 및 버전 관리
- **STM/LTM 분리**: 단기 및 장기 기억 분리 관리

## 주요 API 엔드포인트

### 1. 시스템 상태
- `GET /api/v1/health` - API 서버 상태 확인
- `GET /api/info` - API 정보 조회

### 2. 메모리 블록 관리
- `POST /api/v1/blocks` - 새 메모리 추가
- `GET /api/v1/blocks` - 블록 목록 조회
- `GET /api/v1/blocks/{id}` - 특정 블록 조회
- `GET /api/v1/search` - 키워드 검색

### 3. 단기 기억(STM)
- `GET /api/v1/stm` - 최근 단기 기억 조회
- `POST /api/v1/stm` - 단기 기억 추가
- `DELETE /api/v1/stm` - 단기 기억 초기화

### 4. 프롬프트 생성
- `POST /api/v1/prompt` - 관련 메모리를 포함한 프롬프트 생성

### 5. 유틸리티
- `POST /api/v1/process` - 텍스트 처리 (키워드/태그 추출)
- `GET /api/v1/verify` - 블록체인 무결성 검증

## 설치 방법

### PyPI에서 설치 (v0.6.1)

```bash
# 기본 설치
pip install greeum==0.6.1

# 모든 선택적 기능 포함 설치
pip install greeum[all]==0.6.1

# 특정 기능만 설치
pip install greeum[faiss]==0.6.1  # FAISS 벡터 검색
pip install greeum[transformers]==0.6.1  # BERT, KeyBERT
pip install greeum[openai]==0.6.1  # OpenAI 임베딩
```

## Python 클라이언트 사용법

### 기본 클라이언트 (MemoryClient)

```python
from greeum.client import MemoryClient

# 클라이언트 초기화
client = MemoryClient(
    base_url="http://localhost:5000",
    timeout=30,
    max_retries=3
)

# 메모리 추가
response = client.add_memory(
    context="사용자가 Python 프로그래밍을 좋아합니다",
    keywords=["Python", "프로그래밍", "선호도"],
    importance=0.8
)

# 메모리 검색
results = client.search_memories(
    query="프로그래밍 선호도",
    mode="hybrid",  # embedding, keyword, temporal, hybrid
    limit=5
)

# 최근 메모리 조회
recent = client.get_recent_memories(limit=10)
```

### 간소화 클라이언트 (SimplifiedMemoryClient)

외부 LLM 통합을 위한 간단한 인터페이스:

```python
from greeum.client import SimplifiedMemoryClient

client = SimplifiedMemoryClient(base_url="http://localhost:5000")

# 메모리 추가 (자동으로 키워드 추출)
result = client.add("회의가 내일 오후 3시로 변경되었습니다", importance=0.9)

# 메모리 검색
memories = client.search("회의 일정", limit=3)

# LLM 프롬프트용 문자열 생성
context = client.remember("내일 일정", limit=5)
print(context)
# 출력: 
# [기억 1, 2025-05-18] 회의가 내일 오후 3시로 변경되었습니다
# [기억 2, 2025-05-17] 내일 점심 약속이 있습니다
```

## 실제 통합 예제

### 1. OpenAI GPT와 통합

```python
import openai
from greeum.client import SimplifiedMemoryClient

class MemoryGPT:
    def __init__(self, openai_key, greeum_url="http://localhost:5000"):
        self.client = openai.Client(api_key=openai_key)
        self.memory = SimplifiedMemoryClient(base_url=greeum_url)
    
    def chat(self, user_message):
        # 1. 관련 메모리 검색
        memories = self.memory.remember(user_message, limit=5)
        
        # 2. 시스템 프롬프트에 메모리 포함
        system_prompt = f"""당신은 기억력이 뛰어난 AI 어시스턴트입니다.

과거 대화 기록:
{memories}

위 정보를 참고하여 일관성 있게 답변하세요."""
        
        # 3. GPT 호출
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        
        ai_response = response.choices[0].message.content
        
        # 4. 대화 내용 저장
        self.memory.add(
            f"User: {user_message}\nAssistant: {ai_response}",
            importance=0.7
        )
        
        return ai_response
```

### 2. LangChain 메모리 통합

```python
from langchain.memory import BaseMemory
from greeum.client import SimplifiedMemoryClient

class GreeumLangChainMemory(BaseMemory):
    """LangChain과 Greeum 통합을 위한 커스텀 메모리"""
    
    def __init__(self, greeum_url="http://localhost:5000"):
        self.client = SimplifiedMemoryClient(base_url=greeum_url)
        self.memory_key = "chat_history"
    
    @property
    def memory_variables(self):
        return [self.memory_key]
    
    def load_memory_variables(self, inputs):
        # 사용자 입력과 관련된 메모리 검색
        query = inputs.get("input", "")
        memories = self.client.remember(query, limit=5)
        
        return {self.memory_key: memories}
    
    def save_context(self, inputs, outputs):
        # 대화 내용을 Greeum에 저장
        user_input = inputs.get("input", "")
        ai_output = outputs.get("output", "")
        
        conversation = f"Human: {user_input}\nAI: {ai_output}"
        self.client.add(conversation, importance=0.6)
    
    def clear(self):
        # 메모리 초기화는 Greeum API에서 직접 수행
        pass
```

### 3. FastAPI 웹 서비스 통합

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from greeum.client import SimplifiedMemoryClient, ConnectionFailedError

app = FastAPI(title="Memory-Enhanced Chat API")
memory = SimplifiedMemoryClient()

class ChatRequest(BaseModel):
    user_id: str
    message: str
    save_memory: bool = True

class ChatResponse(BaseModel):
    response: str
    memories_used: list
    memory_saved: bool

@app.post("/chat", response_model=ChatResponse)
async def chat_with_memory(request: ChatRequest):
    try:
        # 사용자별 메모리 검색
        query = f"user:{request.user_id} {request.message}"
        memories = memory.search(query, limit=5)
        
        # 여기서 실제 AI 응답 생성 로직 구현
        # response = generate_ai_response(request.message, memories)
        response = f"메모리 기반 응답: {len(memories)}개의 관련 기억을 찾았습니다."
        
        # 대화 저장
        memory_saved = False
        if request.save_memory:
            result = memory.add(
                f"[{request.user_id}] Q: {request.message} A: {response}",
                importance=0.5
            )
            memory_saved = result["success"]
        
        return ChatResponse(
            response=response,
            memories_used=[m["content"] for m in memories[:3]],
            memory_saved=memory_saved
        )
        
    except ConnectionFailedError:
        raise HTTPException(status_code=503, detail="메모리 서비스 연결 실패")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    health = memory.get_health()
    if not health["success"]:
        raise HTTPException(status_code=503, detail=health["error"])
    return health
```

## 에러 처리

Greeum 클라이언트는 다음 예외들을 발생시킵니다:

```python
from greeum.client import (
    ConnectionFailedError,  # 서버 연결 실패
    RequestTimeoutError,    # 요청 타임아웃
    AuthenticationError,    # 인증 실패 (401, 403)
    APIError               # 기타 API 오류
)

try:
    result = client.add_memory("테스트")
except ConnectionFailedError:
    # 서버 연결 실패 처리
    print("Greeum 서버에 연결할 수 없습니다")
except RequestTimeoutError:
    # 타임아웃 처리
    print("요청 시간이 초과되었습니다")
except APIError as e:
    # API 오류 처리
    print(f"API 오류 발생: {e.status_code} - {e}")
```

## 성능 최적화

### 1. 연결 재사용
```python
# 클라이언트 인스턴스를 전역으로 생성하여 재사용
memory_client = SimplifiedMemoryClient()

def process_messages(messages):
    # 동일한 클라이언트 인스턴스 사용
    for msg in messages:
        memory_client.add(msg)
```

### 2. 배치 처리
```python
# 여러 메모리를 수집 후 한 번에 처리
memories_to_add = []

for item in data:
    memories_to_add.append({
        "content": item["text"],
        "importance": calculate_importance(item)
    })

# 배치로 추가 (현재는 개별 처리, 향후 배치 API 추가 예정)
for memory in memories_to_add:
    client.add(memory["content"], memory["importance"])
```

### 3. 캐싱
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_search(query: str, limit: int = 5):
    """자주 사용되는 검색 쿼리 캐싱"""
    return memory_client.search(query, limit)
```

## 환경 설정

### Docker Compose 예제

```yaml
version: '3.8'

services:
  greeum:
    image: greeum:latest
    ports:
      - "5000:5000"
    environment:
      - TRANSFORMERS_OFFLINE=1
      - HF_HUB_OFFLINE=1
    volumes:
      - ./data:/app/data
      - ./results:/app/results
    
  chat-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GREEUM_URL=http://greeum:5000
    depends_on:
      - greeum
```

### 환경 변수

```bash
# .env 파일
GREEUM_URL=http://localhost:5000
GREEUM_TIMEOUT=30
GREEUM_MAX_RETRIES=3
GREEUM_AUTH_TOKEN=your-optional-auth-token
```

## 모니터링 및 로깅

```python
import logging
from greeum.client import SimplifiedMemoryClient

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("greeum.integration")

class MonitoredMemoryClient(SimplifiedMemoryClient):
    """모니터링 기능이 추가된 메모리 클라이언트"""
    
    def add(self, content, importance=None):
        start_time = time.time()
        try:
            result = super().add(content, importance)
            elapsed = time.time() - start_time
            logger.info(f"메모리 추가 성공: {elapsed:.2f}초, 블록 {result.get('block_index')}")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"메모리 추가 실패: {elapsed:.2f}초, 오류: {e}")
            raise
```

## 주요 작업 내역

1. **API 엔드포인트 분석**: Flask 기반 REST API 구조 분석 완료
2. **클라이언트 라이브러리**: MemoryClient와 SimplifiedMemoryClient 구현
3. **에러 처리**: 재시도 로직과 다양한 예외 클래스 구현
4. **통합 예제**: OpenAI, LangChain, FastAPI 통합 코드 제공
5. **문서화**: API_USAGE.md 파일에 상세 사용법 문서화
6. **v0.6.1 배포**: PyPI에 최신 버전 배포 완료 (2025-06-12)

## v0.6.1 주요 개선사항

### 성능 개선
- **Import 속도 향상**: Lazy loading 적용으로 패키지 import 시간 대폭 단축
- **시작 시간 단축**: sentence-transformers 타임아웃 문제 해결

### 버그 수정
- greeum 패키지 import 문제 해결
- API health 엔드포인트 버전 동기화
- KeyBERT lazy loading 구현으로 startup 지연 해결

### 새로운 기능
- CLAUDE.md 개발 가이드 추가
- API_USAGE.md 상세 문서 추가
- 기본 기능 테스트 스크립트 추가

## 다음 단계 추천

1. **배치 API 추가**: 여러 메모리를 한 번에 추가하는 엔드포인트
2. **웹소켓 지원**: 실시간 메모리 업데이트 알림
3. **GraphQL API**: 더 유연한 쿼리 지원
4. **메트릭 수집**: Prometheus 등을 통한 성능 모니터링
5. **SDK 개발**: 다양한 언어(JavaScript, Go, Java) 클라이언트 라이브러리