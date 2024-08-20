<template>
	<div class="page-wrapper">
		<div class="content-wrapper">
			<h1 v-if="!userStartedChat">Hello! What do you have on your mind?</h1>
			<div
				v-else
				class="chat-messages-box"
				ref="chatMessagesBox"
			>
				<div
					v-for="(message, index) in chatMessages"
					:key="index"
					class="message"
					:class="{
						'eve-message': message.who === 'eve',
						'user-message': message.who === 'user',
						typing: message.isTyping,
					}"
				>
					<div class="message-who">{{ message.who }}</div>
					<div class="message-box">
						{{ message.typingText || message.message }}
					</div>
				</div>
			</div>
			<div
				style="
					position: fixed;
					width: 100%;
					background-color: white;
					height: 85px;
					bottom: 0;
				"
			>
				<div class="user-input-wrapper">
					<input
						type="text"
						v-model="userInput"
						@keydown.enter="sendMessage"
					/>
					<div
						class="send-btn"
						@click="sendMessage"
						:class="eveThinking ? 'disabled' : 'active'"
					>
						<font-awesome-icon :icon="['fas', 'arrow-up']" />
					</div>
				</div>
			</div>
		</div>
	</div>
</template>


<script>
export default {
	name: "mainWindow",
	data() {
		return {
			items: [],
			userInput: "",
			userStartedChat: false,
			chatMessages: [],
			eveThinking: false,
		};
	},

	watch: {
		chatMessages() {
			this.$nextTick(() => {
				const chatBox = this.$refs.chatMessagesBox;
				if (chatBox) {
					chatBox.scrollTop = chatBox.scrollHeight;
				}
			});
		}
	},

	methods: {
		async sendMessage() {
			if (this.userInput !== "") {
				this.userStartedChat = true;

				// User's message
				this.chatMessages.push({
					who: "user",
					message: this.userInput,
				});

				this.userInput = "";
				this.eveThinking = true;

				// Simulate Eve thinking
				//await sleep(1000);

				// Simulate Eve typing response
				const eveMessage = {
					who: "eve",
					message: "",
					typingText: "",
					isTyping: true,
				};

				this.chatMessages.push(eveMessage);
				await this.typeText(
					eveMessage,
					"Eve's generated response, typing character by character."
				);

				eveMessage.isTyping = false;
				this.eveThinking = false;
			}
		},

		async typeText(messageObject, fullText) {
			for (let i = 0; i < fullText.length; i++) {
				messageObject.typingText += fullText[i];

				this.$forceUpdate();

				await sleep(5);
			}
			messageObject.message = fullText;
			messageObject.typingText = null;
		},
	},
};

function sleep(ms) {
	return new Promise((resolve) => setTimeout(resolve, ms));
}
</script>

<style scoped lang="scss">
* {
	font-family: "Courier New", Courier, monospace;
}

#app {
	margin-top: 0 !important;
}

h1 {
	padding: 0;
}

div {
	font-size: 18px;
}

input {
	border: none;
	height: 100%;
	width: 500px;
	outline: none;
	padding: 0px 10px;
	color: rgb(82, 82, 82);
	background-color: #f3e8e1;
	border-radius: 10px;
	font-size: 18px;
}

.page-wrapper {
	display: flex;
	flex-direction: column;
	overflow-y: auto; /* Enable scrolling for the entire page */
}

.content-wrapper {
	flex: 1; /* Fill available space */
	display: flex;
	flex-direction: column;
	justify-content: center; /* Center content vertically */
	align-items: center; /* Center content horizontally */
	padding-bottom: 100px; /* Space for the fixed input at the bottom */
}

.chat-messages-box {
	width: 40%;
	height: 80%; /* Set a fixed height */
	display: flex;
	flex-direction: column;
	gap: 20px;
	align-items: flex-start; /* Align messages to the left for Eve */
	overflow-y: auto; /* Enable vertical scrolling */
}

.user-message {
	align-self: flex-end; /* Align user messages to the right */
}

.user-message .message-box {
	background-color: #a7d4d2;
	color: white;
}

.eve-message .message-box {
	background-color: #f0f0f0;
	color: black;
	border: 1px solid #dcdcdc;
}

.message {
	display: flex;
	flex-direction: column;
	align-items: flex-start;
	max-width: 100%;
	text-align: left;
}

.message-box {
	background-color: #a7d4d2;
	color: white;
	border-radius: 10px;
	padding: 10px 20px;
	word-wrap: break-word;
	white-space: pre-wrap;
	max-width: 100%;
	box-sizing: border-box;
	position: relative; /* Required for the typing cursor */
}

.message-who {
	font-weight: bold;
	margin-bottom: 5px;
}

.user-message .message-box {
	background-color: #a7d4d2;
	color: white;
}

.eve-message .message-box {
	background-color: #f0f0f0;
	color: black;
	border: 1px solid #dcdcdc;
}

.message-box.typing::after {
	content: "|";
	position: absolute;
	right: -10px;
	animation: blink 1s infinite;
	opacity: 1;
}

@keyframes blink {
	0%,
	100% {
		opacity: 0;
	}
	50% {
		opacity: 1;
	}
}

.user-input-wrapper {
	position: fixed;
	bottom: 10px; /* Adjust the distance from the bottom */
	left: 50%;
	transform: translateX(-50%);
	border-radius: 10px;
	display: flex;
	align-items: center;
	width: fit-content;
	border: 1px solid #f3e8e1;
	height: 35px;
	padding: 10px;
	background-color: white;
	margin-bottom: 10px;
}

.send-btn {
	display: flex;
	justify-items: center;
	align-items: center;
	transition: 0.15s;
	cursor: pointer;
	margin-left: 10px;
	border-radius: 10px;
	background-color: #f3e8e1;
}

.send-btn:hover {
	background-color: #a7d4d2;
	color: white;
}

.send-btn svg {
	padding: 10px;
	width: 16px;
	height: 16px;
}

.send-btn.disabled {
	cursor: not-allowed;
	background-color: #e4e4e4;
	color: #8a8a8a;
}

.send-btn.disabled:hover {
	background-color: #e4e4e4;
	color: #8a8a8a;
}
</style>
