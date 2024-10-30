package com.hawk.blindtestockbe.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import software.amazon.awssdk.core.exception.SdkClientException;
import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeClient;
import software.amazon.awssdk.services.bedrockruntime.model.*;

@Slf4j
@Service
@RequiredArgsConstructor
public class AiService {
    private final BedrockRuntimeClient bedrockRuntimeClient;
    private final String MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0";
    private final String SYSTEM_PROMPT = "답변을 할때는 정보만 순서를 매겨서 알려주고 주가동향은 제외해줘";

    public String send(String message) {
        Message requestMessage = Message.builder()
                .content(ContentBlock.fromText(message))
                .role(ConversationRole.USER)
                .build();

        SystemContentBlock systemContentBlock = SystemContentBlock.builder()
                .text(SYSTEM_PROMPT)
                .build();

        try {
            ConverseResponse response = bedrockRuntimeClient.converse(request -> request
                    .modelId(MODEL_ID)
                    .messages(requestMessage)
                    .system(systemContentBlock)
                    .inferenceConfig(config -> config
                            .maxTokens(512)
                            .temperature(0.5F)
                            .topP(0.9F)));

            return response.output().message().content().get(0).text();
        } catch (SdkClientException e) {
            log.error(e.toString(), e);
            throw new RuntimeException(e);
        }
    }
}
