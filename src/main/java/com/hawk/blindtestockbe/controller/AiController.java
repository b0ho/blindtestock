package com.hawk.blindtestockbe.controller;

import com.hawk.blindtestockbe.model.AiRequest;
import com.hawk.blindtestockbe.service.AiService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController
@RequiredArgsConstructor
public class AiController {
    private final AiService aiService;

    @PostMapping("/ai")
    public ResponseEntity<String> sendMessage(@RequestBody AiRequest aiRequest) {
        String aiMessage = aiService.send(aiRequest.message());

        return ResponseEntity.ok(aiMessage);
    }
}
