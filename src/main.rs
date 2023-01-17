use std::fs;
use teloxide::{prelude::*, types::ParseMode, utils::command::BotCommands};

mod flag;
mod sub;

#[derive(BotCommands, Clone)]
#[command(rename_rule = "lowercase")]
enum Command {
    #[command(description = "flag[10]")]
    Flag,
    #[command(description = "POV")]
    Sub,
}

async fn answer(bot: Bot, msg: Message, cmd: Command) -> ResponseResult<()> {
    match cmd {
        Command::Flag => {
            let flag = flag::get_flag().await;
            bot.send_message(msg.chat.id, flag)
                .parse_mode(ParseMode::MarkdownV2)
                .await?;
        }
        Command::Sub => {
            let sub = sub::get_sub().await;
            bot.send_message(msg.chat.id, sub)
                .parse_mode(ParseMode::MarkdownV2)
                .await?;
        }
    }
    Ok(())
}

#[tokio::main]
async fn main() {
    simple_logger::init_with_level(log::Level::Debug).unwrap();
    log::info!("Starting flag10 bot...");
    let token = fs::read_to_string(".token").expect("Failed to read token");
    let bot = Bot::new(token);
    bot.set_my_commands(Command::bot_commands()).await.unwrap();
    Command::repl(bot, answer).await;
}
