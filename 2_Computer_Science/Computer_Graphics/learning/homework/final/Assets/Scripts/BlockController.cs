using UnityEngine;

public class BlockController : MonoBehaviour
{
    [SerializeField] private float fallTime = 1f;
    [SerializeField] private Vector3 rotationPoint = Vector3.zero;
    
    private float lastFallTime;
    public bool IsActive { get; private set; } = true;
    public bool IsPaused = false;

    private void Update()
    {
        if (!IsActive || IsPaused) return;

        if (Time.time - lastFallTime > fallTime)
        {
            Fall();
            lastFallTime = Time.time;
        }
    }

    private void Fall()
    {
        transform.position += Vector3.down;

        if (!GridManager.Instance.IsValidMove(this))
        {
            transform.position += Vector3.up;
            LockBlock();
        }
    }

    public void MoveHorizontal(Vector3 direction)
    {
        if (!IsActive) return;

        transform.position += direction;
        if (!GridManager.Instance.IsValidMove(this))
        {
            transform.position -= direction;
        }
    }

    public void Rotate(Vector3 axis)
    {
        if (!IsActive) return;

        transform.RotateAround(transform.TransformPoint(rotationPoint), axis, 90);
        if (!GridManager.Instance.IsValidMove(this))
        {
            transform.RotateAround(transform.TransformPoint(rotationPoint), axis, -90);
        }
    }

    public void QuickDrop()
    {
        if (!IsActive) return;

        while (GridManager.Instance.IsValidMove(this))
        {
            transform.position += Vector3.down;
        }
        transform.position += Vector3.up;
        LockBlock();
    }

    private void LockBlock()
    {
        IsActive = false;
        GridManager.Instance.AddToGrid(this);
        SpawnManager.Instance.SpawnBlock();
    }
}