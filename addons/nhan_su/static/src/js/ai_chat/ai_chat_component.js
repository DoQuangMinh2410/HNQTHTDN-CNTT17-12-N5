/** @odoo-module **/

import { registry } from "@web/core/registry";
const { Component, hooks, useState } = owl;
const { onWillStart, onMounted, useRef } = hooks;
import { useService } from "@web/core/utils/hooks";

class AIChat extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.messageListRef = useRef("messageList");
        this.state = useState({
            conversations: [],
            activeId: null,
            messages: [],
            inputValue: "",
            isTyping: false,
        });

        onWillStart(async () => {
            await this.loadConversations();
        });

        onMounted(() => {
            this.scrollToBottom();
        });

        this.handleDelete = this.handleDelete.bind(this);
    }

    async handleDelete(ev) {
        ev.stopPropagation();
        const id = parseInt(ev.currentTarget.dataset.id);
        await this.deleteConversation(ev, id);
    }

    async loadConversations() {
        const result = await this.rpc("/web/dataset/call_kw", {
            model: "ai_assistant",
            method: "search_read",
            args: [[]],
            kwargs: {
                fields: ["id", "question", "create_date"],
                order: "create_date desc",
            },
        });
        this.state.conversations = result;
    }

    async selectConversation(id) {
        this.state.activeId = id;
        const result = await this.rpc("/web/dataset/call_kw", {
            model: "ai_assistant",
            method: "read",
            args: [[id]],
            kwargs: {
                fields: ["id", "question", "answer"],
            },
        });
        this.state.messages = result;
        this.scrollToBottom();
    }

    async createNewChat() {
        const id = await this.rpc("/web/dataset/call_kw", {
            model: "ai_assistant",
            method: "create",
            args: [{ question: "Hỏi AI điều gì..." }],
            kwargs: {},
        });
        await this.loadConversations();
        await this.selectConversation(id);
    }

    async deleteConversation(ev, id) {
        ev.stopPropagation(); // Prevent selecting the chat when clicking delete
        if (!confirm("Bạn có chắc chắn muốn xóa cuộc trò chuyện này?")) return;

        await this.rpc("/web/dataset/call_kw", {
            model: "ai_assistant",
            method: "unlink",
            args: [[id]],
            kwargs: {},
        });

        if (this.state.activeId === id) {
            this.state.activeId = null;
            this.state.messages = [];
        }
        await this.loadConversations();
    }

    async sendMessage() {
        if (!this.state.inputValue.trim() || this.state.isTyping) return;

        const currentId = this.state.activeId;
        const question = this.state.inputValue;
        this.state.inputValue = "";
        this.state.isTyping = true;

        // Update the question field in the database
        // If it's the first real question, this will set the conversation title
        await this.rpc("/web/dataset/call_kw", {
            model: "ai_assistant",
            method: "write",
            args: [[currentId], { question: question }],
            kwargs: {},
        });

        // Add to local UI immediately for responsiveness
        this.state.messages = [{ id: 'temp-' + Date.now(), question: question }];
        this.scrollToBottom();

        // Trigger AI processing on the backend
        try {
            await this.rpc("/web/dataset/call_kw", {
                model: "ai_assistant",
                method: "action_ask_ai",
                args: [[currentId]],
                kwargs: {},
            });
        } catch (e) {
            console.error("AI Error", e);
            this.state.messages[0].answer = "Đã có lỗi xảy ra. Vui lòng thử lại.";
        }

        this.state.isTyping = false;
        
        // Refresh sidebar and chat content
        await this.loadConversations();
        await this.selectConversation(currentId);
    }

    async setQuickQuery(text) {
        this.state.inputValue = text;
        await this.sendMessage();
    }

    onInputKeydown(ev) {
        if (ev.key === "Enter") {
            this.sendMessage();
        }
    }

    scrollToBottom() {
        if (this.messageListRef.el) {
            this.messageListRef.el.scrollTop = this.messageListRef.el.scrollHeight;
        }
    }
}

AIChat.template = "nhan_su.AIChat";

registry.category("actions").add("nhan_su.ai_chat_action", AIChat);

export default AIChat;
