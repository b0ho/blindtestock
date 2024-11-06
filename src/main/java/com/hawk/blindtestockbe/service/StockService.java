package com.hawk.blindtestockbe.service;

import com.hawk.blindtestockbe.model.StockRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.time.LocalDate;
import java.util.HashMap;
import java.util.Map;

@Slf4j
@Service
@RequiredArgsConstructor
public class StockService {

    public Map<LocalDate, Double> getHistoricalStockPrices(StockRequest stockRequest) {
        Map<LocalDate, Double> stockPrices = new HashMap<>();
        try {
            ProcessBuilder processBuilder = new ProcessBuilder("python", "fetch_stock_data.py", stockRequest.symbol(), stockRequest.startDate(), stockRequest.endDate());
            processBuilder.redirectErrorStream(true);
            Process process = processBuilder.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line);
            }

            JSONObject json = new JSONObject(output.toString());
            for (String key : json.keySet()) {
                LocalDate date = LocalDate.parse(key);
                Double price = json.getDouble(key);
                stockPrices.put(date, price);
            }
        } catch (Exception e) {
            log.error("Error fetching data from Python script", e);
        }
        return stockPrices;
    }
}