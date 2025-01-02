using UnityEngine;
using TMPro;

public class ScoreManager : MonoBehaviour
{
    public static ScoreManager Instance { get; private set; }

    [SerializeField] private TextMeshProUGUI scoreText;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    private void UpdateScoreDisplay()
    {
        if (scoreText != null)
        {
            int score = GridManager.Instance.linesCleared * 100;
            scoreText.text = $"Score: {score}";
        }
    }

    private void Update()
    {
        UpdateScoreDisplay();
    }
}