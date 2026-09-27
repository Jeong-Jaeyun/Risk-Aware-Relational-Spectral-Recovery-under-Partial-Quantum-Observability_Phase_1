# supplementary file 리비전
---

# 현재 supplementary의 강점

## 1. Main text boundary calibration을 잘 받쳐줌

예:

- “not a foundations-level theory”
- “finite data-object construction”
- “metric trajectory representation”
- “interpretive tools rather than necessary assumptions”

이런 표현들 매우 좋다. `supplementary-file.pdf`

특히 S3:

> “tangent vectors, geodesic curves ... are interpretive tools rather than necessary computational assumptions”

이 문장 좋다. `supplementary-file.pdf`

이게 reviewer의:
> “너 manifold claim 증명했냐?”

공격을 차단한다.

---

# 2. S4는 꽤 강하다

현재 S4는 사실상:
- admissibility
- thresholds
- recovery objective
- stage separation

을 전부 formal하게 설명한다. `supplementary-file.pdf`

이건 좋아.

특히:

> “maximum rather than average”

설명은 reviewer 대응용으로 매우 좋다. `supplementary-file.pdf`

왜냐면:
“왜 max violation?”
질문에 대한 justification이 들어가 있기 때문이다.

---

# 3. S6 operating-zone 분석 좋다

이 부분 꽤 좋아졌다.

특히:

> “The negative operating-zone result indicates that this Boolean criterion is too coarse...”

좋다. `supplementary-file.pdf`

negative result를:
- 실패 ❌
- ablation evidence ✅

로 사용하고 있다.

이건 논문 신뢰도를 올린다.

---

# 4. S8 threshold diagnostics 매우 중요함

이건 reviewer 방어에서 상당히 중요해질 거다. `supplementary-file.pdf`

왜냐면 reviewer가 거의 확실하게:

- “threshold arbitrary”
- “κ arbitrary”
- “u_max hand-tuned”

를 물을 가능성이 높기 때문.

근데 지금:
- κ sweep
- u_max sweep
- saturation interpretation

이 이미 들어가 있다.

좋다.

---

# 그런데 지금 supplementary의 핵심 문제

지금 supplementary는:

## “왜 필요한지”보다
## “뭘 했는지”

설명이 더 많다.

즉:
- 수식은 많음
- 구조는 있음
- formalism도 있음

근데 reviewer 관점에서는:

> “왜 이 supplement section이 존재해야 하지?”

가 아직 약간 약하다.

---

# 가장 먼저 수정해야 할 것

# S1~S3 압축 필요

냉정하게 말하면,
현재 QST reviewer 입장에서:

- Wheeler-DeWitt
- manifold
- geodesic
- Christoffel

은 “supporting language” 정도여야 한다.

근데 지금은 조금 비중이 크다. `supplementary-file.pdf`

---

특히 이 부분:

```latex
We use the term relational spectral manifold...
```

이후 설명 길이가 조금 길다. `supplementary-file.pdf`

현재 main paper는 operational framing으로 성공적으로 이동했는데,

supp 일부는 아직:
> “foundational geometry paper”

의 잔향이 남아있다.

---

# 추천 방향

## S1
현재 길이 유지 가능.

왜냐면:
- consistency condition
- finite clock limitation

설명 필요함.

괜찮다.

---

## S2
좋다.
여긴 유지 추천.

특히 Weyl perturbation bound는 reviewer 설득에 도움 된다. `supplementary-file.pdf`

---

## S3
여기 조금 줄이는 게 좋다.

특히:
- tangent vectors
- Christoffel
- smooth manifold ambiguity

부분.

지금은:
> “우린 geometric intuition을 제공하지만 computational assumption은 아니다”

정도면 충분하다.

현재는 살짝 길다.

---

# 가장 중요한 수정 포인트

# S4를 더 “engineering-like”하게 강화해야 함

왜냐면 reviewer는 결국:
> “controller actually works?”
를 본다.

---

현재 S4는 formalism 설명은 좋은데,

다음이 부족하다:

- 왜 Stage-1만 main result에 사용했는가
- 왜 conservative application rule이 중요한가
- 왜 Stage-2는 diagnostic-only인가

이 부분 justification을 더 강화해야 한다.

---

지금 이 문장:

> “This two-stage design keeps the paper-facing operator auditable”

좋다. `supplementary-file.pdf`

근데 조금 더 밀어도 된다.

예:

- avoids hidden optimization flexibility
- prevents post-hoc candidate shaping
- preserves row-level interpretability

같은 operational justification 추가 가능.

---

# 매우 중요한 포인트 하나

현재 supplementary에서:

## “why relational over ordinary smoother?”
방어가 아직 부족하다.

이건 main에서도 완전 해결된 건 아니었는데,
supp에서 더 보강해야 한다.

---

추천:

S2 or S3에 짧게 추가:

- ordinary temporal smoother는 external ordering 기반
- current framework는 internal conditional family 기반
- admissibility penalties jointly constrained
- reference-anchor compatibility included

정도.

길게 말할 필요 없다.

딱 reviewer 공격 방어용만.

---

# Figures는 매우 좋다

S1/S2 회로도 깔끔하다. `supplementary-file.pdf`

좋은 점:
- “toy simulation”
느낌 줄이고,
- “actual protocol”
느낌 준다.

이건 꽤 중요하다.

---

# 지금 supplementary의 실제 역할

현재 supplementary는:

## “증명”
이 아니라

## “claim calibration + auditability evidence”

역할을 해야 한다.

그리고 지금 거의 그 방향까지 왔다.

---

# 냉정한 현재 상태

현재 supplementary는:

### 강함
- calibration
- thresholds
- intervention diagnostics
- operating-zone evidence
- ablations
- negative controls

### 아직 위험
- geometry language slightly heavy
- manifold flavor 잔존
- relational necessity defense not fully explicit

이다.

---