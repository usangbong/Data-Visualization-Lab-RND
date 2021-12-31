using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class toTransparent : MonoBehaviour
{
    public List<Material> baseMaterialList;
    public List<Material> transparentMaterialList;

    private List<Material> thisMaterial;

    private void Start()
    {
        thisMaterial = baseMaterialList;
    }

    public void toTransparentMaterial()
    {
        thisMaterial = transparentMaterialList;
        changeMaterial();
    }

    public void toBaseMaterial()
    {
        thisMaterial = baseMaterialList;
        changeMaterial();
    }

    void changeMaterial()
    {
        var childList = transform.childCount;
        for (var i = 0; i < childList; i++)
        {
            var child = transform.GetChild(i);
            var mat = thisMaterial[i];
            child.GetComponent<MeshRenderer>().material = mat;
        }
    }
}
