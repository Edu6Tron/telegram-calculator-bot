from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import ast

# Safe evaluation function using ast
def safe_eval(expr):
    allowed_nodes = (
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.operator, ast.unaryop,
        ast.Load, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv
    )
    try:
        node = ast.parse(expr, mode='eval')
        for subnode in ast.walk(node):
            if not isinstance(subnode, allowed_nodes):
                raise ValueError("Unsupported operation")
        return eval(compile(node, "<string>", "eval"))
    except Exception:
        raise

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧮 *Calculator Bot is online!*\n"
        "Type a math expression or use /calc <expression> (e.g. /calc 2+8/4).\n"
        "For help, type /help.",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 *Calculator Bot Help*\n"
        "How to use this bot:\n"
        "- Use /calc <expression> to calculate (e.g. /calc 13*5-8).\n"
        "- You can also just send a math expression by itself (e.g. 2+2*6/3).\n"
        "- Supports: +, -, *, /, %, ** (exponent), // (floor division).\n"
        "Examples:\n"
        "  /calc 6+2*5\n"
        "  3**3-2\n"
        "- For any text that is not math, bot shows a friendly tip.\n"
        "Type /start to restart the welcome message.",
        parse_mode="Markdown"
    )

async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    expr = " ".join(context.args)
    if not expr:
        await update.message.reply_text("Example: /calc 3*7-2")
        return
    try:
        result = safe_eval(expr)
        await update.message.reply_text(f"{expr} = {result}")
    except Exception:
        await update.message.reply_text("Sorry, invalid or unsupported expression!")

async def echo_math(update: Update, context: ContextTypes.DEFAULT_TYPE):
    expr = update.message.text
    try:
        result = safe_eval(expr)
        await update.message.reply_text(f"{expr} = {result}")
    except Exception:
        await update.message.reply_text("Send a math expression (e.g. 3*7-2/4) or use /calc for help.")

def main():
    app = Application.builder().token("8485066419:AAF0bNuJ12HcA0kzvocBbCVJ4N9D2lygrTM").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("calc", calc))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_math))
    app.run_polling()

if __name__ == "__main__":
    main()
