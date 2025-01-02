using UnityEngine;

public class InputManager : MonoBehaviour
{
    private BlockController activeBlock;
    private Camera mainCamera;

    private void Start()
    {
        mainCamera = Camera.main;
    }

    private void Update()
    {
        // Find the active block if not already assigned
        if (activeBlock == null || !activeBlock.IsActive)
        {
            activeBlock = FindFirstObjectByType<BlockController>();
            return;
        }

        // Handle horizontal movement
        if (Input.GetKeyDown(KeyCode.LeftArrow) || Input.GetKeyDown(KeyCode.A))
        {
            MoveBlockRelativeToCamera(Vector3.left);
        }
        else if (Input.GetKeyDown(KeyCode.RightArrow) || Input.GetKeyDown(KeyCode.D))
        {
            MoveBlockRelativeToCamera(Vector3.right);
        }
        else if (Input.GetKeyDown(KeyCode.UpArrow) || Input.GetKeyDown(KeyCode.W))
        {
            MoveBlockRelativeToCamera(Vector3.forward);
        }
        else if (Input.GetKeyDown(KeyCode.DownArrow) || Input.GetKeyDown(KeyCode.S))
        {
            MoveBlockRelativeToCamera(Vector3.back);
        }

        // Handle rotation
        else if (Input.GetKeyDown(KeyCode.Z))
        {
            activeBlock.Rotate(Vector3.right);
        }
        else if (Input.GetKeyDown(KeyCode.X))
        {
            activeBlock.Rotate(Vector3.up);
        }
        else if (Input.GetKeyDown(KeyCode.C))
        {
            activeBlock.Rotate(Vector3.forward);
        }

        // Handle quick drop
        else if (Input.GetKeyDown(KeyCode.Space))
        {
            activeBlock.QuickDrop();
        }
    }

    private void MoveBlockRelativeToCamera(Vector3 direction)
    {
        if (mainCamera == null) return;

        // Get the camera's forward and right vectors, ignoring Y component
        Vector3 cameraForward = mainCamera.transform.forward;
        cameraForward.y = 0;
        cameraForward.Normalize();

        Vector3 cameraRight = mainCamera.transform.right;
        cameraRight.y = 0;
        cameraRight.Normalize();

        // Calculate the movement direction relative to the camera
        Vector3 moveDirection = Vector3.zero;

        if (direction == Vector3.forward)
            moveDirection = cameraForward;
        else if (direction == Vector3.back)
            moveDirection = -cameraForward;
        else if (direction == Vector3.right)
            moveDirection = cameraRight;
        else if (direction == Vector3.left)
            moveDirection = -cameraRight;

        // Round the move direction to the nearest axis
        moveDirection = RoundDirectionToAxis(moveDirection);

        activeBlock.MoveHorizontal(moveDirection);
    }

    private Vector3 RoundDirectionToAxis(Vector3 direction)
    {
        float x = Mathf.Abs(direction.x);
        float z = Mathf.Abs(direction.z);

        if (x > z)
        {
            return new Vector3(Mathf.Sign(direction.x), 0, 0);
        }
        else
        {
            return new Vector3(0, 0, Mathf.Sign(direction.z));
        }
    }
}