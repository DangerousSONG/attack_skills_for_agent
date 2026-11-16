---
name: captcha-bypass-methodology
description: "Methodology for bypassing and solving image captchas / click captchas. Use when a target's login, registration, password reset, or SMS sending endpoints are protected by image captchas, click captchas, or slider captchas that need to be recognized or bypassed. Covers captcha type identification, OCR / captcha-solving platform recognition, click coordinate captcha simulation, captcha logic bypass (reuse/reflection/empty value), rate limit bypass, and authorization boundaries"
zh-signals: "图片与点击式验证码绕过与识别方法论，涵盖类型识别、OCR/打码平台与逻辑绕过。信号:验证码,绕过,点击验证码,OCR,打码,滑块"
when-to-use: "Use when a target's login, registration, password-reset, or SMS endpoint is protected by image, click, or slider captchas that need to be recognized or bypassed."
metadata:
  tags: "captcha,image captcha,click captcha,click,captcha,bypass,recognition,ocr,captcha solving,slider,login,brute force,captcha bypass,unlock,assessment"
  category: "exploit"
---

# Image / Click Captcha Bypass and Recognition

## Applicable Scenarios

Use when login, registration, password reset, SMS sending, and similar endpoints are gated by a captcha.

## Phase 1: Captcha Type Identification

| Type | Characteristics | Bypass Approach |
|------|------|---------|
| Image digit/letter | 4-6 character image | OCR / captcha-solving platform / logic bypass |
| Click-based (click captcha) | Click the requested text/graphic in the image | Coordinate parsing + simulated click |
| Slider | Drag the puzzle piece | Trajectory simulation / gap detection |
| Arithmetic/Chinese text | Directly readable | Regex extraction and direct answer |

## Phase 2: Recognition and Automated Solving

1. **OCR recognition**: use tesseract or a captcha-solving platform to recognize image captchas
2. **Click captcha**: parse the coordinates of the prompt text and click by coordinate (simulate with selenium/requests)
3. **Slider**: detect the gap position, generate a drag trajectory, and bypass frontend trajectory validation

## Phase 3: Logic Bypass (Try This First)

1. **Captcha reuse**: the same code works multiple times
2. **Captcha reflection**: the code is returned directly in the response/JS
3. **Empty value/parameter removal**: set code to empty, remove the captcha parameter
4. **Universal captcha**: a fixed value (e.g. 0000, 8888)
5. **Concurrency bypass**: the captcha is not invalidated after validation, replay it concurrently
6. **Frontend-only validation**: validated only in JS, call the backend API directly to bypass it

## Phase 4: Rate Limit Bypass

- The captcha sending/validation endpoint is rate limited: rotate IPs, pollute parameters, use concurrency
- When brute-forcing a captcha, watch out for account lockouts or IP bans

## Authorization Boundary

- Authorized penetration testing only
- Control the rate when brute-forcing to avoid impacting the business

## Related Skills

- Password reset / SMS verification code logic → password-reset-methodology
