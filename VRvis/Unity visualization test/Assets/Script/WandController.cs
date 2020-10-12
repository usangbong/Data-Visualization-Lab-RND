using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WandController : MonoBehaviour
{
    public GameObject cam;

    public float moveSpeed;
    public SteamVR_TrackedObject TrackedObj;
    private SteamVR_Controller.Device wand { get { return SteamVR_Controller.Input((int)TrackedObj.index); } }

    private GameObject collidingObject;
    private GameObject objectInHand;

    public Transform triggeredObj;
    public Transform selectedObj;
    public bool isTriggerDown;

    public Vector2 BeforeTouchPos;
    public Vector2 TouchPos;

    private void Start()
    {
        TrackedObj = GetComponent<SteamVR_TrackedObject>();
        BeforeTouchPos = wand.GetAxis();
        TouchPos = BeforeTouchPos;
    }
    void Update()
    {
        BeforeTouchPos = TouchPos;
        TouchPos = wand.GetAxis();

        if (TouchPos.x - BeforeTouchPos.x > 0)
        {
            cam.transform.Translate(Vector3.right * moveSpeed * Time.deltaTime);
        }

        else if (TouchPos.x - BeforeTouchPos.x < 0)
        {
            cam.transform.Translate(Vector3.left * moveSpeed * Time.deltaTime);
        }

        if (TouchPos.y - BeforeTouchPos.y > 0)
        {
            cam.transform.Translate(Vector3.forward * moveSpeed * Time.deltaTime);
        }

        else if (TouchPos.y - BeforeTouchPos.y < 0)
        {
            cam.transform.Translate(Vector3.back * moveSpeed * Time.deltaTime);
        }

        if (wand.GetHairTriggerDown())
        {
            isTriggerDown = true;
            if (triggeredObj == null) return;

            selectedObj = triggeredObj;
            selectedObj.parent = transform;

            Rigidbody r = selectedObj.GetComponent<Rigidbody>();
            r.useGravity = false;
            r.isKinematic = true;
        }
        if (wand.GetHairTriggerUp())
        {
            isTriggerDown = false;
            if (selectedObj == null) return;

            selectedObj.parent = null;
            //Rigidbody r = selectedObj.GetComponent<Rigidbody>();

            selectedObj = null;
        }

        if (wand.GetPress(SteamVR_Controller.ButtonMask.Grip))
        {
            Debug.Log("SideButtonDown");
        }

        if (wand.GetPress(SteamVR_Controller.ButtonMask.Touchpad))
        {
            Debug.Log("TouchpadDown");
        }

        
    }
    private void OnTriggerEnter(Collider other)
    {
        if(other.gameObject.layer == LayerMask.NameToLayer("Object")) {
            if (triggeredObj != null) return;
            triggeredObj = other.transform;
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.gameObject.layer == LayerMask.NameToLayer("Object"))
        {
            if (triggeredObj == null) return;
            triggeredObj = null;
        }
    }
}
