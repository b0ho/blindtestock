package com.hawk.blindtestockbe.model;

public record StockRequest (
        String symbol,
        String startDate,
        String endDate
){
}
