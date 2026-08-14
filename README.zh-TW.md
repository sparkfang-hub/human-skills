# Human Skills

**給那些人生沒有附說明書的時刻。**

大部分 Agent Skill 都在教 AI 寫程式、部署或操作工具。Human Skills 想處理的是另一種情境：

- 你睡不著，但現在最不需要的是十點睡眠衛教；
- 你正在氣頭上，手指已經停在傳送鍵；
- 對方還沒回覆，你的腦袋已經把五小時演成一整季影集。

這不是把 AI 變成心理師，也不是讓 AI 替你決定人生。它只是教 AI 在人最容易亂掉的時候，先講少一點、慢一點、不要亂診斷、不要陪著腦補，並且在安全有疑慮時把人帶回真正的人類支援。

> Human Skills 應該幫你回到生活，不是想辦法把你留在聊天室。

## 第一批 Skill

| Skill | 使用情境 |
| --- | --- |
| [`sleep-with-me`](skills/sleep-with-me/) | 睡不著、半夜醒來、腦袋停不下來，需要低刺激陪伴。 |
| [`dont-text-them`](skills/dont-text-them/) | 很想立刻傳一則可能會後悔、施壓、連發或乞求回覆的訊息。 |
| [`stop-the-spiral`](skills/stop-the-spiral/) | 反覆推演、災難化、把未知直接當成最壞答案。 |

## 安裝

查看 repository 內可安裝的 Skill：

```bash
npx skills add sparkfang-hub/human-skills --list
```

安裝其中一個：

```bash
npx skills add sparkfang-hub/human-skills \
  --skill sleep-with-me \
  --global
```

Claude Code 也可以把這個 repository 加成 marketplace：

```text
/plugin marketplace add sparkfang-hub/human-skills
/plugin install human-skills@human-skills
```

需要上傳檔案的環境，可以使用 [`dist/`](dist/) 裡的 `.skill` 檔。

## 核心原則

Human Skills 要溫暖，但不假裝親密；要有幫助，但不假裝治療；要承認未知，而不是替別人的沉默算命。

它不會協助繞過封鎖、騷擾、追蹤、情緒勒索、威脅自傷換取回覆，也不會要求使用者把 AI 當成唯一能理解自己的人。

完整內容請看英文版 [README](README.md)、[設計原則](docs/design-principles.md) 與 [安全模型](docs/safety-model.md)。
