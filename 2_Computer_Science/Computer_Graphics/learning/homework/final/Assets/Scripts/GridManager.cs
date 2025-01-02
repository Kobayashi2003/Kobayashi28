using UnityEngine;

public class GridManager : MonoBehaviour
{
    public static GridManager Instance { get; private set; }

    public int width = 10;
    public int height = 15;
    public int depth = 10;

    public int linesCleared = 0;

    private Transform[,,] grid;

    public GameObject BottomPlane;
    public GameObject Face01, Face02, Face03, Face04;

    private void Awake()
    {
        // Singleton pattern implementation
        if (Instance == null)
        {
            Instance = this;
            InitializeGrid();
        }
        else
        {
            Destroy(gameObject);
        }
    }

    private void InitializeGrid()
    {
        grid = new Transform[width, height, depth];
    }

    public bool IsValidMove(Vector3[] positions)
    {
        foreach (Vector3 pos in positions)
        {
            Vector3 roundedPos = RoundVector(pos);
            if (!IsInsideGrid(roundedPos) || GridPositionOccupied(roundedPos))
            {
                return false;
            }
        }
        return true;
    }

    public bool IsValidMove(BlockController block)
    {
        // Convert block's child positions to an array
        Vector3[] positions = new Vector3[block.transform.childCount];
        int i = 0;
        foreach (Transform child in block.transform)
        {
            positions[i] = child.position;
            i++;
        }
        return IsValidMove(positions);
    }

    public bool IsValidMove(ShadowController shadow)
    {
        Vector3[] positions = new Vector3[shadow.transform.childCount];
        for (int i = 0; i < shadow.transform.childCount; i++)
        {
            positions[i] = shadow.transform.GetChild(i).position;
        }
        return IsValidMove(positions);
    }

    private bool IsInsideGrid(Vector3 pos)
    {
        return pos.x >= 0 && pos.x < width &&
               pos.y >= 0 && pos.y < height &&
               pos.z >= 0 && pos.z < depth;
    }

    private bool GridPositionOccupied(Vector3 pos)
    {
        return grid[(int)pos.x, (int)pos.y, (int)pos.z] != null;
    }


    public void AddToGrid(BlockController block)
    {
        foreach (Transform child in block.transform)
        {
            Vector3 pos = RoundVector(child.position);
            grid[(int)pos.x, (int)pos.y, (int)pos.z] = child;
        }
        CheckForLines();
    }

    private void CheckForLines()
    {
        for (int y = 0; y < height; y++)
        {
            if (CheckPlane(y))
            {
                linesCleared++;
            }
        }
    }

    private bool CheckPlane(int y)
    {
        bool planeCleared = false;

        // Check X lines
        for (int x = 0; x < width; x++)
        {
            if (IsLineX(x, y))
            {
                ClearLineX(x, y);
                planeCleared = true;
            }
        }

        // Check Z lines
        for (int z = 0; z < depth; z++)
        {
            if (IsLineZ(y, z))
            {
                ClearLineZ(y, z);
                planeCleared = true;
            }
        }

        if (planeCleared)
        {
            DropBlocksAbove(y);
        }

        return planeCleared;
    }


    private bool IsLineX(int x, int y)
    {
        for (int z = 0; z < depth; z++)
        {
            if (grid[x, y, z] == null)
            {
                return false;
            }
        }
        return true;
    }

    private bool IsLineZ(int y, int z)
    {
        for (int x = 0; x < width; x++)
        {
            if (grid[x, y, z] == null)
            {
                return false;
            }
        }
        return true;
    }

    private void ClearLineX(int x, int y)
    {
        for (int z = 0; z < depth; z++)
        {
            Destroy(grid[x, y, z].gameObject);
            grid[x, y, z] = null;
        }
    }

    private void ClearLineZ(int y, int z)
    {
        for (int x = 0; x < width; x++)
        {
            Destroy(grid[x, y, z].gameObject);
            grid[x, y, z] = null;
        }
    }

    private void DropBlocksAbove(int clearedY)
    {
        for (int y = clearedY; y < height - 1; y++)
        {
            for (int x = 0; x < width; x++)
            {
                for (int z = 0; z < depth; z++)
                {
                    if (grid[x, y + 1, z] != null)
                    {
                        grid[x, y, z] = grid[x, y + 1, z];
                        grid[x, y, z].transform.position += Vector3.down;
                        grid[x, y + 1, z] = null;
                    }
                }
            }
        }
    }

    private Vector3 RoundVector(Vector3 v)
    {
        return new Vector3(Mathf.Round(v.x), Mathf.Round(v.y), Mathf.Round(v.z));
    }
}