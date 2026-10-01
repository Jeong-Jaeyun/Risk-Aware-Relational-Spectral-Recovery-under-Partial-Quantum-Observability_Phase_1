# 독립 추가실험 R1: 물리적 일관성과 식별 가능성

2026-09-27. 결과를 보기 전에 설계와 통과 기준을 고정한다. 외부 사전등록은 아니다. 기존 제출 grid와 구분하며, 이 실험만으로 C3R 또는 일반적인 unknown-state QEC의 우월성을 주장하지 않는다.

## 목적과 순서

1. 전역 Hamiltonian 제약과 conditional dynamics를 동시에 만족하는 최소 clock–logical-system 모델을 확인한다.
2. 기존 graph/spectrum이 실제로 관측 정보를 보존하는지 negative/positive control로 검사한다.
3. 독립 held-out logical state와 finite-shot partial observations에서 동일 정보·동일 예산 기준선을 비교한다.
4. 이 단계에서 식별성이 없는 표현은 C3R의 성능 실험에 넣어 개선을 주장하지 않는다. 유효한 후보·위험 점수의 후속 설계가 필요하다.

## 물리 모델

각 repetition code의 logical Pauli를 X_L, Z_L이라 한다.

\[
H_C=\omega Z_C,\quad
H_S=-\omega(n_xX_L+n_zZ_L),\quad \omega=0.8.
\]

`aligned`: n=(0,0,1); `tilted`: n=(1,0,1)/sqrt(2).

tilted 모델은 logical X를 포함하므로 물리적으로 3-body Pauli interaction을 요구한다. 이상적으로 알려진 engineered logical Hamiltonian을 가정하며, 기존 H_S=0 설정의 단순 수치 수정이나 무료 자원으로 설명하지 않는다. 추가 3-body **관측**을 사용하지는 않지만 dynamics 자원은 달라진다.

n·sigma의 고유상태 |n+>, |n->와 임의의 logical 초기상태 |psi>=c+|n+>+c-|n->를 사용해

\[
|\Psi\rangle=c_+|0\rangle_C|n+\rangle_L+c_-|1\rangle_C|n-\rangle_L
\]

를 구성한다. (H_C+H_S)|Psi>=0이며, |tau>=exp(-i H_C tau)|+>에 조건화하면 exp(-i H_S tau)|psi>가 나와야 한다.

8개 label tau_k=k*pi/(8*omega), k=0,...,7을 사용한다. 이는 서로 직교하는 8개의 clock 상태가 아니다. E_k=(2/8)|tau_k><tau_k|인 유효 POVM이며 합이 I다. 이 모델에서 각 label 확률은 1/8이다. 전체 prepared copy 수를 먼저 정하고 label별 수를 multinomial로 배정하므로 postselection 비용을 숨기지 않는다.

## 정보와 식별 가능성

측정은 code-aligned population 한 축이다: bitflip은 physical Z, phaseflip은 physical X. 이상적인 code subspace에서 한 qubit의 결과로 동일 축의 pair population을 추정할 수 있다. code subspace라는 모델 가정을 명시한다. 이번 R1에는 물리적 data noise나 손상된 syndrome decoder를 넣지 않고, clock-label erasure와 binary population readout error만 넣는다.

초기 logical Bloch vector r에 대한 측정 평균은 z_k=M_k r이다. `aligned`는 rank 1로 phase를 식별할 수 없고, `tilted`의 전체 clock grid는 rank 3이어야 한다. 이것은 known engineered dynamics와 여러 clock outcome의 결합 효과다.

기존 bitflip mutual-information graph와 phaseflip coherence-absolute graph는 z와 -z를 구분하지 못한다. 따라서 r과 -r의 전체 관측 trajectory가 graph/spectrum에서 같아지는 negative control을 반드시 포함한다.

positive control은 W_ij=(1+z_k)/2, i!=j인 occupation graph다. 이는 기존 방법을 대신해 우월성을 주장하려는 새 알고리즘이 아니라 **부호 정보를 보존하는 대조 표현**이다. spectrum은 {0,3w,3w}이고 z=trace(L)/3-1로 되돌릴 수 있으므로 raw population과 정확히 같은 정보다. spectral 결과가 raw 결과보다 좋게 나오면 독립적인 이점으로 해석하지 않고 구현/비교 오류를 먼저 의심한다.

## 비교 방법 — 같은 측정 기록 공유

- raw mixed-state weighted least squares: observed label별 counts로 가중해 r을 추정하고 Bloch ball에 투영한다.
- signed-occupation spectral least squares: 위 spectrum에서 z를 복원한 뒤 **동일한** 회귀·투영을 적용한다. raw와 수치적으로 같아야 하는 positive control.
- raw pure-state least squares: full-rank일 때만 pure-state prior로 radial normalization. rank 부족 시 mixed-state 추정을 유지한다.
- raw nearest reference: raw population trajectory로 고정 reference bank에서 선택.
- legacy spectral nearest reference: 기존 code별 graph/spectrum으로 같은 bank에서 선택. 안정적인 first-index tie rule(1e−12)을 적용한다.

모든 estimator는 측정 counts, clock label, known Hamiltonian, 고정 reference bank만 받는다. test target, ideal target density, 실제 readout error 확률은 입력으로 받지 않는다. fidelity 계산만 별도 evaluator가 test target을 사용한다. 알려진 pure-state 가정의 유무를 구분해 보고한다.

## 분할과 grid

- Reference bank: 고정 RNG로 만든 16개 Bloch 방향과 그 antipode, 총 32개 pure state.
- Test: 별도 RNG의 32개 방향과 antipode, 총 64개 held-out pure state. bank와 정확히 겹치지 않는지 확인한다.
- code: bitflip, phaseflip. 같은 기록을 공유하는 basis-equivalent 검증이며 독립 표본 두 배로 취급하지 않는다.
- dynamics: aligned, tilted.
- 총 prepared copies/target: 128, 512, 2048.
- retained clock labels: 1, 4, 8 (8개 중 균등하게 mask 선택). 삭제된 label의 copies도 비용에 포함한다.
- binary population readout flip probability: 0, 0.05, 0.15. estimator에 제공하지 않으며 detector calibration correction을 하지 않는다.
- measurement seeds: 12개. target 생성 seed 및 measurement seed는 분리한다.
- 총 1,296개 job × 64개 target = 82,944개 평가 행. 각 방법이 같은 행의 데이터를 공유한다.

antipodal pair의 시뮬레이션은 counts와 clock mask를 공유하고 population 성공 횟수를 서로 보수로 사용한다. 각 주변분포는 올바른 binomial이며, pair 내 common-random-number coupling을 명시한다. pair는 독립 표본 2개로 취급하지 않는다. 이 대조는 sign-blind representation의 식별 불가능성을 finite-shot에서도 정확히 검증한다.

## 사전 통과 기준

- 전역 제약 residual, conditional density와 Schrödinger evolution 차이, POVM completeness 오차 각각 <1e−10.
- clock 인접 label의 geometric distance >0.1. eigenstate clock negative control은 0이어야 한다.
- tilted full-grid measurement design rank=3; aligned rank=1.
- held-out noiseless tilted raw/signed-spectral reconstruction infidelity <1e−10.
- legacy graph의 antipodal spectral 차이 <1e−10. 그 표현의 nearest-reference는 antipodal pair 평균 fidelity 0.5여야 한다. 이것은 finite bank 튜닝으로 해결되지 않는 정보 손실 진단이다.
- raw mixed LS와 signed-spectral LS의 prediction 차이 <1e−10. 성능 이득이 아니라 정보/구현의 동일성 검사다.
- finite-shot의 rank-deficient/zero-count 사례를 삭제하지 않는다. 최소노름 추정으로 평가하고 별도 집계한다.
- 실패 시 강건성 또는 C3R 효과를 주장하는 다음 단계로 자동 진행하지 않는다.

평균 fidelity, q05 fidelity, rank-deficient 비율, accepted/prepared copies를 보고한다. 신뢰구간은 측정 seed를 먼저 평균낸 뒤 독립 target **pair** 단위 5,000회 paired bootstrap으로 계산한다. 이는 해당 target 분포에 대한 실험적 불확실성이며 시스템 전반의 일반 보장이 아니다. code별·grid별로 분리하고 유리한 cell만 선택하지 않는다.

간단한 보고서 표는 미리 고정한 `8개 label 전부 유지, readout error=0` slice에서 두 code·두 dynamics·세 copies 값을 모두 보여준다. 전체 108개 grid cell은 별도 JSON으로 보존한다. 이는 보고서 표시를 위한 선택이며, 다른 조건의 결과를 숨기거나 이 표만으로 일반화하지 않는다.

## 해석의 경계

이것은 동일하게 준비한 여러 복사본에서의 state/trajectory estimation 실험이다. 단일 unknown quantum state를 보존하는 QEC channel 또는 entanglement fidelity 실험이 아니다. B 상태 재준비를 QEC로 바꿔 부르지 않는다. R1의 성공은 새 물리·관측 모델에서 다음 recovery 실험을 할 자격을 확보하는 것이지 논문의 원래 claim을 자동으로 복구하는 것이 아니다.

참고: [Page–Wootters 전역 제약과 conditional dynamics](https://www.nature.com/articles/s41467-021-21782-4), [세-qubit pure state의 reduced-state 식별성 연구](https://arxiv.org/abs/quant-ph/0207109). 위 finite-clock 모델, negative/positive control, 자원 계산은 본 실험에서 직접 구성하고 수치 검증한다. generic state에 대한 식별성 결과를 GHZ형 특수 상태에 무조건 적용하지 않는다.
