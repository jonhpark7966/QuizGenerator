
# Subject - Daily Quiz Generator

- Motivation & Purpose
	- 많은 사람들이 뉴스를 읽는 데에 시간을 할애함
	- 재밋는 뉴스, 좋은 뉴스 퀴즈 시스템을 만들자


# Architecture

![[news_arch.svg]]

## News crawler
- Input Source
	- NEWSAPI.org
	- Other Web sources
	- Youtube ? Podcast ?
- Output
	- Source URL & Metadata (title, time, category, ...)

## News Analyzer
- Role
	- Curate or filtering the articles (재미, 좋은)
	- Keyword tagging
	- Summarization
	- Translation
	- ...
- In / Out
	- Crawled news -> Structured data (JSON)
- Implementation
	- Agent (?)
## AI Quiz Generation
- 
- CrewAI for high-level
- LangGraph for low-level, if need it

## Quiz Data Format Architecture

- question
- Answer
- source url
- tag

## Quiz UI
- crossword puzzle
- 객관식 문항