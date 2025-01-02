using UnityEngine;

public class SpawnManager : MonoBehaviour
{
    public static SpawnManager Instance { get; private set; }

    [SerializeField] private GameObject[] blockPrefabs;
    [SerializeField] private GameObject[] shadowPrefabs;
    [SerializeField] private Vector3 spawnPosition = new Vector3(5, 10, 5);

    private void Awake()
    {
        // Singleton pattern implementation
        if (Instance == null)
        {
            Instance = this;
        }
        else
        {
            Destroy(gameObject);
        }
    }

    public void SpawnBlock()
    {
        // Validate prefab arrays
        if (blockPrefabs == null || blockPrefabs.Length == 0)
        {
            Debug.LogError("Block prefabs array is empty!");
            return;
        }

        if (shadowPrefabs == null || shadowPrefabs.Length != blockPrefabs.Length)
        {
            Debug.LogError("Shadow prefabs array is missing or doesn't match blocks array!");
            return;
        }

        // Randomly select a block
        int randomIndex = Random.Range(0, blockPrefabs.Length);
        
        // Instantiate block and shadow
        GameObject block = Instantiate(blockPrefabs[randomIndex], spawnPosition, Quaternion.identity);
        GameObject shadow = Instantiate(shadowPrefabs[randomIndex], spawnPosition, Quaternion.identity);

        // Set up block controller
        BlockController blockController = block.GetComponent<BlockController>();
        if (blockController == null)
        {
            Debug.LogError("Block prefab is missing BlockController component!");
            Destroy(block);
            Destroy(shadow);
            return;
        }

        // Set up shadow controller
        ShadowController shadowController = shadow.GetComponent<ShadowController>();
        if (shadowController != null)
        {
            shadowController.SetParentBlock(blockController);
        }
        else
        {
            Debug.LogError("Shadow prefab is missing ShadowController component!");
            Destroy(shadow);
        }

        // Check if the spawn position is valid
        if (!GridManager.Instance.IsValidMove(blockController))
        {
            GameManager.Instance.GameOver();
        }
    }
}