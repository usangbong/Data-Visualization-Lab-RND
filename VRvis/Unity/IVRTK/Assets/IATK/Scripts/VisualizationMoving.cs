using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Valve.VR;

public class VisualizationMoving : MonoBehaviour
{
    public SteamVR_Input_Sources handType;
    public SteamVR_Action_Boolean touchPadPush;
    public SteamVR_Action_Vector2 touchPadPos;
    public SteamVR_Action_Boolean TriggerInput;
    public SteamVR_Action_Boolean GrabInput;

    public GameObject obj;

    Vector2 touchValue;

    float maxPos;

    int select;

    const int NONE = 0;
    const int UP = 1;
    const int DOWN = 2;
    const int RIGHT_ROTATE = 3;
    const int LEFT_ROTATE = 4;

    public float moveSpeed = 0.01f;
    public float rotateSpeed = 1f;

    private void Update()
    {
        if(TriggerInput.GetState(handType))
        {
            obj.transform.position = new Vector3(obj.transform.position.x, obj.transform.position.y, obj.transform.position.z - moveSpeed);
        }

        if(GrabInput.GetState(handType))
        {
            obj.transform.position = new Vector3(obj.transform.position.x, obj.transform.position.y, obj.transform.position.z + moveSpeed);
        }

        if (touchPadPush.GetState(handType))
        {
            touchValue = touchPadPos.GetAxis(handType);

            select = NONE;
            maxPos = 0;
            if (Mathf.Abs(touchValue.x) > maxPos)
            {
                maxPos = Mathf.Abs(touchValue.x);

                if (touchValue.x < 0) select = LEFT_ROTATE;
                else select = RIGHT_ROTATE;
            }

            if (Mathf.Abs(touchValue.y) > maxPos)
            {
                if (touchValue.y < 0) select = DOWN;
                else select = UP;
            }

            switch (select)
            {
                case NONE:
                    return;
                case UP:
                    obj.transform.position = new Vector3(obj.transform.position.x, obj.transform.position.y + moveSpeed, obj.transform.position.z);
                    break;
                case DOWN:
                    obj.transform.position = new Vector3(obj.transform.position.x, obj.transform.position.y - moveSpeed, obj.transform.position.z);
                    break;
                case RIGHT_ROTATE:
                    obj.transform.rotation = Quaternion.Euler(new Vector3(obj.transform.rotation.eulerAngles.x, obj.transform.rotation.eulerAngles.y - rotateSpeed, obj.transform.rotation.eulerAngles.z));
                    break;
                case LEFT_ROTATE:
                    obj.transform.rotation = Quaternion.Euler(new Vector3(obj.transform.rotation.eulerAngles.x, obj.transform.rotation.eulerAngles.y + rotateSpeed, obj.transform.rotation.eulerAngles.z));
                    break;
                default:
                    break;
            }
        }

    }
}
