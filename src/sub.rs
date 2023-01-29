use rand::seq::SliceRandom;
use scraper::{Html, Selector};
use serde::Deserialize;
use std::time::{Duration, Instant};
use teloxide::utils::markdown;
use tokio::sync::Mutex;

#[derive(Clone, Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct Sub {
    id: u64,
    contest_id: u64,
    problem: Problem,
    verdict: String,
}

#[derive(Clone, Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct Problem {
    index: String,
    name: String,
}

async fn get_list() -> Result<Vec<Sub>, Box<dyn std::error::Error>> {
    #[derive(Deserialize)]
    struct Response {
        result: Vec<Sub>,
    }

    lazy_static::lazy_static! {
        static ref CACHE: Mutex<Option<(Instant, Vec<Sub>)>> = Mutex::new(None);
    }

    let mut lock = CACHE.lock().await;
    let now = Instant::now();

    if let Some((time, subs)) = &*lock {
        if now.duration_since(*time) < Duration::from_secs(3600 * 24) {
            return Ok(subs.clone());
        }
    }

    let url = "https://codeforces.com/api/user.status?handle=TheScrasse";
    let resp = reqwest::get(url).await?.json::<Response>().await?;
    let subs = resp.result;

    *lock = Some((now, subs.clone()));
    Ok(subs)
}

pub async fn get_sub() -> Result<String, Box<dyn std::error::Error>> {
    let list = get_list().await?;
    let Sub {
        id,
        contest_id,
        problem,
        verdict,
    } = list
        .choose(&mut rand::thread_rng())
        .ok_or("No submissions")?;

    log::info!("Getting sub {} from contest {}", id, contest_id);

    // let cookies = reqwest::CookieJar::new();

    let url = format!(
        "https://codeforces.com/contest/{}/submission/{}",
        contest_id, id
    );
    let html = reqwest::get(&url).await?.text().await?;
    let soup = Html::parse_document(&html);
    let code = soup
        .select(&Selector::parse("#program-source-text").expect("Failed to parse selector"))
        .next()
        .ok_or("Failed to find #program-source-text")?
        .text()
        .next()
        .ok_or("Failed to find text in #program-source-text")?;

    Ok(format!(
        "{} {} \\- {} \\- *{}*\n`{}`",
        contest_id,
        problem.index,
        markdown::escape(&problem.name),
        markdown::escape(verdict),
        markdown::escape_code(code)
    ))
}
