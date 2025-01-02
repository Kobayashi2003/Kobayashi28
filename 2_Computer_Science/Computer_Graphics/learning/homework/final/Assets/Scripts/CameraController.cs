using UnityEngine;

public class CameraController : MonoBehaviour
{
    [SerializeField] private float sensitivity = 5.0f;
    [SerializeField] private float smoothSpeed = 30.0f;
    [SerializeField] private float minVerticalRotation = -30f;
    [SerializeField] private float maxVerticalRotation = 60f;
    [SerializeField] private float distanceMultiplier = 1.5f;
    [SerializeField] private float minDistance = 30f;
    [SerializeField] private float maxDistance = 50f;
    
    private Vector3 centerPoint;
    private float orbitDistance;
    private Vector2 currentRotation;

    private void Start()
    {
        GridManager gridManager = GridManager.Instance;
        if (gridManager == null)
        {
            Debug.LogError("GridManager not found!");
            return;
        }

        centerPoint = new Vector3(
            gridManager.width * 0.5f,
            gridManager.height * 0.5f,
            gridManager.depth * 0.5f
        );

        float maxDimension = Mathf.Max(gridManager.width, gridManager.height, gridManager.depth);
        orbitDistance = Mathf.Clamp(maxDimension * distanceMultiplier, minDistance, maxDistance);

        Vector3 directionFromCenter = (transform.position - centerPoint).normalized;
        currentRotation.x = Mathf.Asin(directionFromCenter.y) * Mathf.Rad2Deg;
        currentRotation.y = Mathf.Atan2(directionFromCenter.x, directionFromCenter.z) * Mathf.Rad2Deg;

        UpdateCameraPosition();
    }

    private void Update()
    {
        if (Input.GetMouseButton(1))
        {
            float mouseX = Input.GetAxis("Mouse X") * sensitivity;
            float mouseY = Input.GetAxis("Mouse Y") * sensitivity;

            currentRotation.x = Mathf.Clamp(currentRotation.x - mouseY, minVerticalRotation, maxVerticalRotation);
            currentRotation.y += mouseX;

            UpdateCameraPosition();
        }

        float scroll = Input.GetAxis("Mouse ScrollWheel");
        if (scroll != 0)
        {
            orbitDistance = Mathf.Clamp(orbitDistance - scroll * 5f, minDistance, maxDistance);
            UpdateCameraPosition();
        }
    }

    private void UpdateCameraPosition()
    {
        float verticalRotation = currentRotation.x * Mathf.Deg2Rad;
        float horizontalRotation = currentRotation.y * Mathf.Deg2Rad;

        Vector3 targetPosition = centerPoint + new Vector3(
            Mathf.Sin(horizontalRotation) * Mathf.Cos(verticalRotation),
            Mathf.Sin(verticalRotation),
            Mathf.Cos(horizontalRotation) * Mathf.Cos(verticalRotation)
        ) * orbitDistance;

        transform.position = Vector3.Lerp(transform.position, targetPosition, smoothSpeed * Time.deltaTime);

        transform.rotation = Quaternion.Slerp(
            transform.rotation,
            Quaternion.LookRotation(centerPoint - transform.position),
            smoothSpeed * Time.deltaTime
        );
    }
}