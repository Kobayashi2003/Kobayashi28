using UnityEngine;

public class ShadowController : MonoBehaviour
{
    private BlockController parentBlock;

    public void SetParentBlock(BlockController block)
    {
        parentBlock = block;
    }

    private void Update()
    {
        if (parentBlock == null || !parentBlock.IsActive)
        {
            Destroy(gameObject);
            return;
        }

        UpdateShadowPosition();
    }

    private void UpdateShadowPosition()
    {
        transform.SetPositionAndRotation(parentBlock.transform.position, parentBlock.transform.rotation);

        do
        {
            transform.position += Vector3.down;
        } while (GridManager.Instance.IsValidMove(this));

        transform.position += Vector3.up;
    }
}