using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }
    
    [Header("Managers")]
    [SerializeField] private SpawnManager spawnManager;
    
    private bool isGameOver;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
            SceneManager.sceneLoaded += OnSceneLoaded;
        }
        else if (Instance != this)
        {
            Destroy(gameObject);
            return;
        }
    }

    private void OnSceneLoaded(Scene scene, LoadSceneMode mode)
    {
        // Find and setup UI buttons in the newly loaded scene
        SetupSceneButtons(scene.name);

        if (scene.name == "GameScene")
        {
            StartGame();
        }
    }

    private void SetupSceneButtons(string sceneName)
    {
        // Find all buttons in the current scene
        Button[] sceneButtons = FindObjectsByType<Button>(FindObjectsSortMode.None);
        
        foreach (Button button in sceneButtons)
        {
            // Remove any existing listeners first
            button.onClick.RemoveAllListeners();
            
            // Add new listeners based on button name
            switch (button.gameObject.name.ToLower())
            {
                case "playbutton":
                    button.onClick.AddListener(() => SceneManager.LoadScene("GameScene"));
                    break;
                case "quitbutton":
                    button.onClick.AddListener(QuitGame);
                    break;
                case "menubutton":
                    button.onClick.AddListener(() => SceneManager.LoadScene("PlayScene"));
                    break;
            }
        }
    }

    private void StartGame()
    {
        isGameOver = false;
        spawnManager = FindFirstObjectByType<SpawnManager>();
        if (spawnManager != null)
        {
            spawnManager.SpawnBlock();
        }
        else
        {
            Debug.LogError("SpawnManager not found in the scene!");
        }
    }

    public void GameOver()
    {
        if (!isGameOver)
        {
            isGameOver = true;
            Debug.Log("Game Over");
            SceneManager.LoadScene("GameOver");
        }
    }

    public void QuitGame()
    {
        #if UNITY_EDITOR
            UnityEditor.EditorApplication.isPlaying = false;
        #else
            Application.Quit();
        #endif
    }

    private void OnDestroy()
    {
        SceneManager.sceneLoaded -= OnSceneLoaded;
    }
}