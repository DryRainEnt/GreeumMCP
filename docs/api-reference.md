# GreeumMCP API 레퍼런스

이 문서는 GreeumMCP가 제공하는 모든 MCP 도구와 리소스의 상세 사양을 설명합니다.

## 목차

- [메모리 관리 도구](#메모리-관리-도구)
  - [add_memory](#add_memory) - 장기 메모리 추가
  - [query_memory](#query_memory) - 의미 기반 검색
  - [retrieve_memory](#retrieve_memory) - ID로 메모리 조회
  - [update_memory](#update_memory) - 메모리 업데이트
  - [delete_memory](#delete_memory) - 메모리 삭제
  - [search_time](#search_time) - 시간 기반 검색
- [단기 메모리 도구](#단기-메모리-도구)
  - [add_stm](#add_stm) - 단기 메모리 추가
  - [get_stm_memories](#get_stm_memories) - 단기 메모리 목록
  - [forget_stm](#forget_stm) - 단기 메모리 삭제
  - [cleanup_expired_memories](#cleanup_expired_memories) - 만료된 메모리 정리
- [유틸리티 도구](#유틸리티-도구)
  - [generate_prompt](#generate_prompt) - 프롬프트 생성
  - [extract_keywords](#extract_keywords) - 키워드 추출
  - [extract_tags](#extract_tags) - 태그 추출
  - [verify_chain](#verify_chain) - 체인 검증
  - [server_status](#server_status) - 서버 상태
- [MCP 리소스](#mcp-리소스)
  - [memory_block](#memory_block-resource) - 개별 메모리 블록
  - [memory_chain](#memory_chain-resource) - 메모리 체인
  - [stm_list](#stm_list-resource) - 단기 메모리 목록
  - [server_config](#server_config-resource) - 서버 설정

---

## 메모리 관리 도구

### add_memory

장기 메모리에 새로운 정보를 저장합니다.

#### 파라미터

| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| content | string | ✓ | 저장할 메모리 내용 |
| keywords | array | | 관련 키워드 목록 |
| tags | array | | 관련 태그 목록 |
| importance | number | | 중요도 (0.0-1.0, 기본값: 0.5) |

#### 반환값

```json
{
  "id": "block_123",
  "block_index": 123,
  "timestamp": "2024-01-01T12:00:00Z",
  "keywords": ["프로젝트", "회의"],
  "tags": ["중요"],
  "importance": 0.8
}
```

#### 예시

```python
result = add_memory(
    content="프로젝트 X의 데드라인이 2월 15일로 연기되었다",
    keywords=["프로젝트X", "데드라인", "연기"],
    tags=["important", "deadline"],
    importance=0.9
)
```

### query_memory

의미적 유사도를 기반으로 관련 메모리를 검색합니다.

#### 파라미터

| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| query | string | ✓ | 검색 쿼리 |
| limit | integer | | 반환할 최대 결과 수 (기본값: 5) |
| min_importance | number | | 최소 중요도 필터 (0.0-1.0) |

#### 반환값

```json
[
  {
    "id": "block_123",
    "content": "프로젝트 X의 데드라인이 2월 15일로 연기되었다",
    "similarity": 0.92,
    "timestamp": "2024-01-01T12:00:00Z",
    "keywords": ["프로젝트X", "데드라인"],
    "importance": 0.9
  }
]
```

### retrieve_memory

특정 ID의 메모리를 조회합니다.

#### 파라미터

| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| memory_id | string | ✓ | 메모리 ID 또는 블록 인덱스 |

#### 반환값

메모리 객체 또는 null

### update_memory

기존 메모리의 중요도나 태그를 업데이트합니다.

#### 파라미터

| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| memory_id | string | ✓ | 메모리 ID 또는 블록 인덱스 |
| importance | number | | 새로운 중요도 (0.0-1.0) |
| tags | array | | 새로운 태그 목록 |

### delete_memory

메모리를 삭제합니다 (주의: 복구 불가).

#### 파라미터

| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| memory_id | string | ✓ | 삭제할 메모리 ID |

### search_time

자연어 시간 표현을 이용한 메모리 검색입니다.

#### 파라미터

| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| query | string | ✓ | 시간 표현이 포함된 검색어 |
| language | string | | 언어 코드 (ko/en/auto, 기본값: auto) |
| margin_hours | integer | | 시간 범위 여유 (기본값: 12) |

#### 반환값

```json
{
  "detected": true,
  "time_expression": "어제",
  "search_range": {
    "from": "2024-01-01T00:00:00Z",
    "to": "2024-01-01T23:59:59Z"
  },
  "blocks": [...]
}
```

#### 지원 시간 표현

- 한국어: "어제", "오늘", "그저께", "지난주", "3일 전"
- 영어: "yesterday", "today", "last week", "3 days ago"
- 날짜: "2024년 1월 1일", "2024-01-01"

---

## 단기 메모리 도구

### add_stm

임시로 기억할 정보를 단기 메모리에 저장합니다.

#### 파라미터

| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| content | string | ✓ | 저장할 내용 |
| ttl_type | string | | 유지 시간 (short/medium/long, 기본값: medium) |
| importance | number | | 중요도 (0.0-1.0, 기본값: 0.5) |

#### TTL 타입

- `short`: 1시간 (임시 정보, 일회성 데이터)
- `medium`: 1일 (당일 작업, 미팅 메모)
- `long`: 1주일 (주간 계획, 진행 중인 작업)

### get_stm_memories

현재 활성화된 단기 메모리 목록을 조회합니다.

#### 파라미터

| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| limit | integer | | 반환할 최대 개수 (기본값: 10) |
| ttl_type | string | | 특정 TTL 타입만 필터 |

### forget_stm

특정 단기 메모리를 즉시 삭제합니다.

#### 파라미터

| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| memory_id | string | ✓ | 삭제할 단기 메모리 ID |

### cleanup_expired_memories

만료된 단기 메모리를 정리합니다.

#### 파라미터

없음

#### 반환값

```json
{
  "cleaned": 5,
  "message": "5개의 만료된 메모리가 정리되었습니다"
}
```

---

## 유틸리티 도구

### generate_prompt

사용자 입력과 관련된 메모리를 포함한 향상된 프롬프트를 생성합니다.

#### 파라미터

| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| user_input | string | ✓ | 사용자 입력 |
| max_blocks | integer | | 포함할 최대 장기 메모리 수 (기본값: 5) |
| max_stm | integer | | 포함할 최대 단기 메모리 수 (기본값: 3) |
| include_stm | boolean | | 단기 메모리 포함 여부 (기본값: true) |

#### 반환값

메모리 컨텍스트가 포함된 향상된 프롬프트 문자열

### extract_keywords

텍스트에서 키워드를 추출합니다.

#### 파라미터

| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| text | string | ✓ | 분석할 텍스트 |
| language | string | | 언어 코드 (ko/en/auto, 기본값: auto) |
| max_keywords | integer | | 최대 키워드 수 (기본값: 10) |

### extract_tags

텍스트에서 태그를 추출합니다.

#### 파라미터

| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| text | string | ✓ | 분석할 텍스트 |
| language | string | | 언어 코드 (ko/en/auto, 기본값: auto) |

### verify_chain

블록체인 무결성을 검증합니다.

#### 파라미터

없음

#### 반환값

```json
{
  "valid": true,
  "total_blocks": 150,
  "message": "체인이 유효합니다"
}
```

### server_status

서버 상태와 통계를 조회합니다.

#### 파라미터

없음

#### 반환값

```json
{
  "status": "healthy",
  "version": "0.2.0",
  "memory_stats": {
    "total_blocks": 150,
    "active_stm": 5,
    "cache_size": 10
  },
  "config": {
    "data_dir": "./data",
    "ttl_short": 3600,
    "ttl_medium": 86400,
    "ttl_long": 604800
  }
}
```

---

## MCP 리소스

### memory_block (Resource)

특정 메모리 블록의 상세 정보를 제공합니다.

#### 엔드포인트

`memory_block/{block_id}`

#### 반환 형식

```json
{
  "id": "block_123",
  "content": "메모리 내용",
  "timestamp": "2024-01-01T12:00:00Z",
  "keywords": ["키워드1", "키워드2"],
  "tags": ["태그1", "태그2"],
  "importance": 0.8,
  "embedding": [...],
  "previous_hash": "abc123...",
  "hash": "def456..."
}
```

### memory_chain (Resource)

전체 메모리 체인 정보를 제공합니다.

#### 엔드포인트

`memory_chain`

#### 반환 형식

```json
{
  "total_blocks": 150,
  "head_block": {...},
  "chain_valid": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### stm_list (Resource)

활성 단기 메모리 목록을 제공합니다.

#### 엔드포인트

`stm_list`

### server_config (Resource)

서버 설정 정보를 제공합니다.

#### 엔드포인트

`server_config`

---

## 에러 처리

모든 도구는 다음과 같은 에러 형식을 반환할 수 있습니다:

```json
{
  "error": "에러 메시지",
  "code": "ERROR_CODE",
  "details": "상세 설명"
}
```

### 일반적인 에러 코드

- `MEMORY_NOT_FOUND`: 요청한 메모리를 찾을 수 없음
- `INVALID_PARAMETER`: 잘못된 파라미터
- `STORAGE_ERROR`: 저장소 관련 오류
- `EMBEDDING_ERROR`: 임베딩 생성 실패

---

## 사용 제한

- 최대 메모리 크기: 1MB/블록
- 최대 키워드 수: 50개/블록
- 최대 태그 수: 20개/블록
- 임베딩 차원: 384

---

## 버전 정보

- 현재 버전: 0.2.0
- MCP 프로토콜 버전: 1.0
- Greeum 엔진 버전: 0.6.0+