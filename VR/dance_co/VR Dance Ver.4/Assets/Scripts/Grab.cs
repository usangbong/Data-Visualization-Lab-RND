using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Valve.VR;

public class Grab : MonoBehaviour
{
    public SteamVR_Input_Sources handType;
    public SteamVR_Action_Boolean grabAction;

    GameObject collidingObject, objectInHand;

    private void Update()
    {
        if(grabAction.GetLastStateDown(handType))
        {
            if(collidingObject)
            {
                GrabObject();
            }
        }

        if(grabAction.GetLastStateUp(handType))
        {
            if(objectInHand)
            {
                ReleaseObject();
            }
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        SetCollidingObject(other);
    }

    private void OnTriggerStay(Collider other)
    {
        SetCollidingObject(other);
    }

    void OnTriggerExit(Collider other)
    {
        if (!collidingObject) return;

        collidingObject = null;
    }

    void SetCollidingObject(Collider col)
    {
        if (collidingObject || !col.GetComponent<Rigidbody>()) return;

        collidingObject = col.gameObject;
    }

    void GrabObject()
    {
        objectInHand = collidingObject;
        collidingObject = null;

        var joint = AddFixedJoint();
        joint.connectedBody = objectInHand.GetComponent<Rigidbody>();
    }

    FixedJoint AddFixedJoint()
    {
        FixedJoint fx = gameObject.AddComponent<FixedJoint>();
        fx.breakForce = 20000;
        fx.breakTorque = 20000;
        return fx;
    }

    void ReleaseObject()
    {
        if(GetComponent<FixedJoint>())
        {
            GetComponent<FixedJoint>().connectedBody = null;
            Destroy(GetComponent<FixedJoint>());
        }

        objectInHand = null;
    }
}
