from app.ml.predictor import predictor


def test_model_classifies_sample_true_and_fake_texts_correctly():
    predictor.load()

    true_text = (
        "A government agency, university, hospital, or research organization announced "
        "a verified public initiative, scientific study, infrastructure project, "
        "healthcare improvement, environmental program, or education initiative. "
        "The report uses neutral language, cites officials or researchers, and does "
        "not contain sensational or extraordinary claims."
    )
    fake_text = (
        "A viral social media post claims an extraordinary event such as impossible "
        "scientific discoveries, unrealistic government giveaways, miracle cures, "
        "secret conspiracies, or supernatural phenomena without evidence or support "
        "from reliable sources."
    )

    true_result = predictor.predict(true_text)
    fake_result = predictor.predict(fake_text)

    assert true_result["label_name"] == "Real"
    assert fake_result["label_name"] == "Fake"
