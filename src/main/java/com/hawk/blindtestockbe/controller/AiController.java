package com.hawk.blindtestockbe.controller;

import com.hawk.blindtestockbe.model.AiRequest;
import com.hawk.blindtestockbe.model.StockRequest;
import com.hawk.blindtestockbe.service.AiService;
import com.hawk.blindtestockbe.service.StockService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.Map;

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

    private final StockService stockService;

    @GetMapping("/stock")
    public Map<LocalDate, Double> getHistoricalStockPrices(
            @RequestBody StockRequest stockRequest) {
        return stockService.getHistoricalStockPrices(stockRequest);
    }
}
